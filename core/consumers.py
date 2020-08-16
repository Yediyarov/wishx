import asyncio
from channels.consumer import AsyncConsumer
import json
from channels.db import database_sync_to_async
from base_user.models import MyUser
from core.models import Reply, Donation, Wish, Like
from django.conf import settings
import os
from django.utils.translation import ugettext_lazy as _


class CommentConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('Connected successufully', event)
        await self.send({
            'type': 'websocket.accept'
        })
        wish_slug = self.scope['url_route']['kwargs']['slug']
        wish_id = await self.get_wish_id(wish_slug)
        self.wish = "thread_{}".format(wish_id)
        await self.channel_layer.group_add(
            self.wish,
            self.channel_name
        )

        # for sending data from back to front
        # await self.send({
        #     'type': 'websocket.send',
        #     'text': 'Hello'
        # })

    # receive data from front
    async def websocket_receive(self, event):
        print('received', event)
        comment_data = event.get('text')
        comment = json.loads(comment_data)
        donation_id = int(comment['donation_id'])
        user = comment['user']
        comment_text = comment['comment_text']

        new_comment = await self.create_comment(donation_id, comment_text, user)

        comment_creation_date = new_comment.since

        if new_comment.user.profile_picture:
            comment_author_picture = new_comment.user.get_profile_picture()
        else:
            comment_author_picture = os.path.join(settings.STATIC_URL, 'wishx/assets/default_user.png')

        comment_author_fullname = new_comment.user.get_full_name()

        comment = {
            'comment_text': comment_text,
            'donation_id': donation_id,
            'full_name': comment_author_fullname,
            'user_picture': comment_author_picture,
            'created_at': comment_creation_date,
            'comment_id': new_comment.pk
        }
        # Send comment to group
        await self.channel_layer.group_send(
            self.wish,
            {
                'type': 'show_comment',
                'text': json.dumps(comment)
            }
        )

    @database_sync_to_async
    def create_comment(self, donation_id, comment, username):
        user = MyUser.objects.get(username=username)
        donation = Donation.objects.get(pk=donation_id)
        reply = Reply.objects.create(user=user, donation=donation, comment=comment)
        return reply

    @database_sync_to_async
    def get_wish_id(self, wish_slug):
        return str(Wish.objects.get(slug=wish_slug).pk)

    async def show_comment(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        print('Websocket disconnected ', event)


# ------------------------------End Comment websocket section--------------------------------------------

class LikeDislikeConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Connected successufully', event)
        await self.send({
            'type': 'websocket.accept'
        })
        wish_slug = self.scope['url_route']['kwargs']['slug']
        wish_id = await self.get_wish_id(wish_slug)
        self.wish = "thread__{}".format(wish_id)
        await self.channel_layer.group_add(
            self.wish,
            self.channel_name
        )

    async def websocket_receive(self, event):
        like_data = event.get('text')
        like_info = json.loads(like_data)
        like_type = like_info['type']
        liked = like_info['liked']
        user = like_info['user']
        item_id = int(like_info['item_id'])

        if like_type == 'donation' and liked:
            await self.delete_like(user, donation_id=item_id)
        elif like_type == 'donation' and not liked:
            await self.create_like(user, donation_id=item_id)

        if like_type == 'comment' and liked:
            await self.delete_like(user, comment_id=item_id)
        elif like_type == 'comment' and not liked:
            await self.create_like(user, comment_id=item_id)

        if like_type == 'donation':
            like_count = await self.get_like_count(donation_id=item_id)
        elif like_type == 'comment':
            like_count = await self.get_like_count(comment_id=item_id)

        final_data = {
            'like_count': like_count,
            'item_id': item_id,
            'type': like_type
        }

        await self.channel_layer.group_send(
            self.wish,
            {
                'type': 'like_donation',
                'text': json.dumps(final_data)
            }
        )

    async def like_donation(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_wish_id(self, wish_slug):
        return str(Wish.objects.get(slug=wish_slug).pk)

    @database_sync_to_async
    def get_like_count(self, donation_id=None, comment_id=None):
        if donation_id is not None:
            return int(Like.objects.filter(donation_id=donation_id).count())
        elif comment_id is not None:
            return int(Like.objects.filter(reply_id=comment_id).count())

    @database_sync_to_async
    def create_like(self, username, donation_id=None, comment_id=None):
        user = MyUser.objects.get(username=username)
        if donation_id is not None:
            like = Like.objects.create(user=user, donation_id=donation_id)
        elif comment_id is not None:
            like = Like.objects.create(user=user, reply_id=comment_id)
        return like

    @database_sync_to_async
    def delete_like(self, username, donation_id=None, comment_id=None):
        user = MyUser.objects.get(username=username)
        if donation_id is not None:
            like = Like.objects.filter(user=user, donation_id=donation_id).first()
            if like:
                like.delete()
        elif comment_id is not None:
            like = Like.objects.filter(user=user, reply_id=comment_id).first()
            if like:
                like.delete()

    async def websocket_disconnect(self, event):
        print('Websocket disconnected ', event)
