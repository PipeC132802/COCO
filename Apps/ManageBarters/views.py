from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from notify.signals import notify
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Apps.ManageBarters.models import Barter, BarterAbout, BarterSkill, BarterMode, BarterInterest, BarterReaction, \
    BarterComment, BarterView
from Apps.ManageBarters.serializer import BarterCommentSerializer
from Apps.ManageUsers.models import Area, UserRelationship, UserInterest, UserSession
from Apps.ManageUsers.signals import retrieve_barters
from COCO.functions import get_place, get_profile_url, get_img_url_from_model, get_notification_and_mark_as_unread
from django.contrib.sessions.models import Session


class BarterApi(generics.CreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        barter = request.GET["barter"]
        try:
            barter = Barter.objects.get(id=barter)
            barter.deleted = True
            barter.save()
            return Response({'Detail': 'Barter deleted'}, status=200)
        except:

            return Response({'Detail': 'Barter not found'}, status=404)

    def put(self, request, *args, **kwargs):
        def update_barter_about(barter, request):
            barter_about = BarterAbout.objects.get(barter=barter)
            barter_about.description = request.data['description']
            barter_about.place = get_place(city=request.data['city'], country=request.data['country'])
            barter_about.save()

        def update_barter_mode(barter, request):
            barter_mode = BarterMode.objects.get(barter=barter)
            barter_mode.mode = request.data['mode']
            barter_mode.save()

        try:
            barter = Barter.objects.get(id=request.data['barter'])
            barter.barter_title = request.data['title']
            barter.edit = True
            barter.save()
            update_barter_about(barter, request)
            update_barter_mode(barter, request)
            self.create_barter_skill(request=request, barter=barter)
            self.create_barter_interest(request=request, barter=barter)
            return Response({'Detail': 'Barter edited successfully'}, status=200)
        except:
            return Response({'Detail': 'Barter not found'}, status=404)

    def post(self, request, *args, **kwargs):
        barter = self.create_barter(request)
        self.create_barter_about(request, barter)
        self.create_barter_skill(request, barter)
        self.create_barter_interest(request, barter)
        self.create_barter_mode(request, barter)
        return Response({'Detail': 'new barter created succesfuly'}, status=200)

    @staticmethod
    def create_barter(request):
        title = request.data['title']
        user = request.user
        return Barter.objects.create(user=user, barter_title=title)

    @staticmethod
    def create_barter_about(request, barter):
        description = request.data['description']
        country = request.data['country']
        city = request.data['city']
        place = get_place(country=country, city=city)
        BarterAbout.objects.create(description=description, place=place, barter=barter)

    def create_barter_skill(self, request, barter):
        skill = request.data['skill']
        area = self.get_area(area=skill)
        if area.exists():
            try:
                BarterSkill.objects.create(area=area[0], barter=barter)
            except:
                barter_skill = BarterSkill.objects.get(barter=barter)
                barter_skill.area = area[0]
                barter_skill.save()

    def create_barter_interest(self, request, barter):
        interest = request.data['interest']
        area = self.get_area(area=interest)
        if area.exists():
            try:
                BarterInterest.objects.create(area=area[0], barter=barter)
            except:
                barter_interest = BarterInterest.objects.get(barter=barter)
                barter_interest.area = area[0]
                barter_interest.save()

    @staticmethod
    def create_barter_mode(request, barter):
        mode = request.data['mode']
        BarterMode.objects.create(mode=mode, barter=barter)

    @staticmethod
    def get_area(area):
        return Area.objects.filter(area=area)


class BarterListApi(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        def get_interest(request):
            return UserInterest.objects.filter(user__username=request.GET['username']).values_list('area__area',
                                                                                                   flat=True).distinct()

        user = User.objects.filter(username=request.GET['username'])
        field = request.GET['field']
        if field == 'profile':
            query = Q(user=user.first(), deleted=False)
            barters_json = self.get_barter_list(query)
        elif field == 'reactions':
            barters_json = self.get_barters_reacted(request)
        elif field == 'recommendations':
            interests = get_interest(request)
            barters_json = self.get_barters_recommendations(interests, request)
        elif field == 'detail' or field == 'search':
            query = Q(id=request.GET['id'])
            barters_json = self.get_barter_list(query)
        else:
            query = Q(user_id__in=self.get_following_users(user.first()), deleted=False)
            barters_json = self.get_barter_list(query)

        return Response(barters_json, status=200)

    @staticmethod
    def get_following_users(user):
        following = list(
            UserRelationship.objects.filter(user_from=user, status=1).values_list('user_to_id', flat=True).distinct())
        if user:
            following.append(user.pk)
        return following

    def get_barter_list(self, query):
        barters = Barter.objects.filter(query).order_by('-created')
        barter_list = []
        for barter in barters:
            barter_about = BarterAbout.objects.get(barter=barter)
            barter_json = {
                'id': barter.pk,
                'user': {
                    'username': barter.user.username,
                    'name': '{0} {1}'.format(barter.user.first_name, barter.user.last_name),
                    'profile_picture': get_profile_url(barter.user)
                },
                'about': barter_about.serializer(),
                'mode': BarterMode.objects.get(barter=barter).mode,
                'skill': BarterSkill.objects.get(barter=barter).area.area,
                'interest': BarterInterest.objects.get(barter=barter).area.area,
                'created': barter.created,
                'edited': barter.edit,
                'title': barter.barter_title,
                'slug': barter.slug,
                'views': self.barter_viewed(barter=barter)
            }
            barter_list.append(barter_json)
        return barter_list

    def barter_viewed(self, barter):

        barter_views = BarterView.objects.filter(barter=barter).first()
        user_request_id = self.request.GET['user_request']
        if user_request_id not in barter_views.users.strip(',').split(
                ',') and barter_views and user_request_id != 'undefined':
            barter_views.store_as_list(user_request_id)
        return barter_views.counter

    @staticmethod
    def get_barters_reacted(request):
        barters_reacted = BarterReaction.objects.filter(user_from__username=request.GET['user'],
                                                        barter__deleted=False).exclude(
            barter__user__username=request.GET['user']).exclude(reaction=0).order_by('-barter__created')
        barter_list = []
        for barter_reacted in barters_reacted:
            barter_about = BarterAbout.objects.get(barter=barter_reacted.barter)
            barter_json = {
                'id': barter_reacted.barter.pk,
                'user': {
                    'username': barter_reacted.barter.user.username,
                    'name': '{0} {1}'.format(barter_reacted.barter.user.first_name,
                                             barter_reacted.barter.user.last_name),
                    'profile_picture': get_profile_url(barter_reacted.barter.user)
                },
                'about': barter_about.serializer(),
                'mode': BarterMode.objects.get(barter=barter_reacted.barter).mode,
                'skill': BarterSkill.objects.get(barter=barter_reacted.barter).area.area,
                'interest': BarterInterest.objects.get(barter=barter_reacted.barter).area.area,
                'created': barter_reacted.barter.created,
                'edited': barter_reacted.barter.edit,
                'title': barter_reacted.barter.barter_title,
                'slug': barter_reacted.barter.slug,
                'reaction': barter_reacted.reaction
            }
            barter_list.append(barter_json)
        return barter_list

    @staticmethod
    def get_barters_recommendations(interests, request):
        barters_skill = BarterSkill.objects.filter(area__area__in=interests, barter__deleted=False).exclude(
            barter__user__username=request.GET['user'])
        barter_list = []
        for barter_skill in barters_skill:
            barter_about = BarterAbout.objects.get(barter=barter_skill.barter)
            barter_json = {
                'id': barter_skill.barter.pk,
                'user': {
                    'username': barter_skill.barter.user.username,
                    'name': '{0} {1}'.format(barter_skill.barter.user.first_name, barter_skill.barter.user.last_name),
                    'profile_picture': get_profile_url(barter_skill.barter.user)
                },
                'about': barter_about.serializer(),
                'mode': BarterMode.objects.get(barter=barter_skill.barter).mode,
                'skill': BarterSkill.objects.get(barter=barter_skill.barter).area.area,
                'interest': BarterInterest.objects.get(barter=barter_skill.barter).area.area,
                'created': barter_skill.barter.created,
                'edited': barter_skill.barter.edit,
                'title': barter_skill.barter.barter_title,
                'slug': barter_skill.barter.slug
            }
            barter_list.append(barter_json)
        return barter_list


class BarterReactionsApi(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        barter_id = request.GET['barter_id']

        reactions = BarterReaction.objects.filter(barter_id=barter_id).exclude(reaction=0)
        reaction_response = {
            'reactions': reactions.count(),
            'types': reactions.values_list('reaction', flat=True).distinct(),
            'comments': BarterComment.objects.filter(barter_id=barter_id, deleted=False).count()
        }
        return Response(reaction_response)


class CreateBarterReactionApi(generics.CreateAPIView, generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        barter_id = request.GET['barter_id']
        reaction = BarterReaction.objects.filter(barter_id=barter_id, user_from=request.user).exclude(reaction=0)
        if reaction.exists():
            return Response({'reaction': reaction[0].reaction})
        else:
            return Response({'reaction': 0})

    def post(self, request, *args, **kwargs):
        def get_query():
            query = Q(recipient=barter_reaction.barter.user, actor_object_id=request.user.pk,
                      target_object_id=barter_reaction.barter.pk, obj_object_id=barter_reaction.pk,
                      verb='Reaccionó a tu trueque', nf_type='reacted_by_one_user')
            return query

        try:
            barter_reaction = BarterReaction.objects.get(barter_id=request.data["barter_id"], user_from=request.user)
            barter_reaction.reaction = request.data["reaction"]
            barter_reaction.save()
            get_notification_and_mark_as_unread(get_query())
        except:
            barter = Barter.objects.get(id=request.data["barter_id"])
            barter_reaction = BarterReaction.objects.create(barter=barter, user_from=request.user,
                                                            reaction=request.data["reaction"])
            if request.user.pk != barter_reaction.barter.user.pk:
                notify.send(request.user, recipient=barter_reaction.barter.user, actor=request.user,
                            target=barter_reaction.barter, obj=barter_reaction,
                            verb='Reaccionó a tu trueque', nf_type='reacted_by_one_user')

        return Response(
            {
                'Detail': 'barter reaction set successfully',
                'reaction': barter_reaction.reaction,
                'user_to': barter_reaction.barter.user.username,
                'user_from': {
                    'username': request.user.username,
                    'name': '{0} {1}'.format(request.user.first_name, request.user.last_name),
                    'profile_picture': get_profile_url(request.user)
                },
                'action': 'Reaccionó a tu trueque',
                'created': datetime.now(),
                'barter': barter_reaction.barter.serializer(),
                'field': 'reaction'
            }
        )


class BarterCommentsApi(generics.CreateAPIView, generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    model = BarterComment
    serializer_class = BarterCommentSerializer

    def post(self, request, *args, **kwargs):
        user_from = request.user
        comment = request.data["comment"]
        photo = request.FILES.get("photo")
        try:
            barter = Barter.objects.get(id=request.data["barter"])
        except:
            return Response({'Detail': 'Barter not found'}, status=404)

        if barter.user != user_from:
            try:
                barter_comment = BarterComment.objects.create(comment=comment.strip(' '), barter=barter,
                                                              user_from=user_from,
                                                              photo=photo)
                notify.send(request.user,
                            recipient=barter_comment.barter.user,
                            actor=request.user,
                            target=barter_comment.barter,
                            obj=barter_comment,
                            verb='Comentó en tu trueque',
                            nf_type='barter_commented')

                return Response({'Detail': 'Comment created successfully',
                                 'user_barter': barter_comment.barter.user.username,
                                 'user_comment': {
                                     'username': request.user.username,
                                     'name': '{0} {1}'.format(request.user.first_name, request.user.last_name),
                                     'profile_picture': get_profile_url(request.user)
                                 },
                                 'action': 'Comentó en tu trueque',
                                 'barter': barter_comment.barter.serializer(),
                                 'comment': {
                                     'text': barter_comment.comment,
                                     'id': barter_comment.pk
                                 },
                                 'field': 'comment'
                                 }, status=200)
            except:
                return Response({'Detail': 'An error have occurred'}, status=500)
        else:
            return Response({'Detail': 'You cannot make a proposal to yourself'}, status=406)

    def get(self, request, *args, **kwargs):
        barter = request.GET["barter"]
        comments = self.get_comments(barter)
        return Response(comments)

    def put(self, request, *args, **kwargs):
        action = request.data['action']
        # TO-DO fix update comment
        response = None
        if action == 'update':
            response = self.update_comment(request)
        elif action == 'accept':
            response = self.just_accepted_status(request)
        return Response(response, status=200)

    def delete(self, request, *args, **kwargs):
        comment = request.GET["comment"]
        try:
            comment = BarterComment.objects.get(id=comment)
            comment.deleted = True
            comment.save()
            return Response({'Detail': 'Comment deleted'}, status=200)
        except:
            return Response({'Detail': 'Comment not found'}, status=404)

    @staticmethod
    def just_accepted_status(request):
        comment = BarterComment.objects.get(id=request.data['comment'])
        comment.accepted = True
        comment.save()
        notify.send(request.user,
                    recipient=comment.user_from,
                    actor=request.user,
                    target=comment,
                    obj=comment.barter,
                    verb='Aceptó tu propuesta',
                    nf_type='accepted_by_user')

        return {'Detail': 'Comment accepted status updated successfully', 'status': comment.accepted,
                'user_comment': comment.user_from.username,
                'user_accept': {
                    'username': request.user.username,
                    'name': '{0} {1}'.format(request.user.first_name, request.user.last_name),
                    'profile_picture': get_profile_url(request.user)
                },
                'action': 'Aceptó tu propuesta',
                'barter': comment.barter.serializer(),
                'comment': {
                    'text': comment.comment,
                    'id': comment.pk
                },
                'field': 'comment'}

    @staticmethod
    def update_comment(request):
        comment = request.data['comment']

        comment_model = BarterComment.objects.get(id=request.data['commentId'])
        comment_model.comment = comment
        comment_model.edited = True
        try:
            photo = request.FILES.get("photo")
            comment_model.photo = photo
        except:
            pass
        comment_model.save()

        return {'Detail': 'Comment updated successfully'}

    @staticmethod
    def get_comments(barter):
        comment_list = []
        comments = BarterComment.objects.filter(barter_id=barter, deleted=False).order_by('-created')
        for comment in comments:
            comment_json = {
                'id': comment.pk,
                'user': {
                    'username': comment.user_from.username,
                    'name': '{0} {1}'.format(comment.user_from.first_name, comment.user_from.last_name),
                    'profile_picture': get_profile_url(comment.user_from)
                },
                'comment': comment.comment,
                'photo': get_img_url_from_model(BarterComment, Q(id=comment.pk)),
                'accepted': comment.accepted,
                'updated': comment.updated,
                'created': comment.created
            }
            comment_list.append(comment_json)
        return comment_list
