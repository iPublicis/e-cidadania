# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Clione Software
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from apps.thirdparty.tagging.fields import TagField
from apps.thirdparty.tagging.models import Tag
from core.spaces.models import Space


class Post(models.Model):

    """
    Model of a news post.
    """
    title = models.CharField(_('Title'), max_length=200,
    help_text=_('Max: 200 characters'))
    description = models.TextField(_('Description'))
    pub_date = models.DateTimeField(_('Date'), auto_now_add=True)
    post_lastup = models.DateTimeField(_('Last update'), auto_now=True)
    author = models.ForeignKey(User, verbose_name=_('Author'), blank=True,
            null=True, help_text=_('Change the user that will figure as the \
                                  author'))
    pub_index = models.BooleanField(_('Publish in index'),
    help_text=_('This will publish the post in the main site page'))
    space = models.ForeignKey(Space, verbose_name=_('Publish in'),
                                   blank=True, null=True,
            help_text=_('If you want to post to the index leave this blank'))
    post_tags = TagField(help_text=_('Insert here relevant words related with the post'))
    views = models.IntegerField(_('Views'), blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return self.title

    def comment_count(self):
        ct = ContentType.objects.get_for_model(Post)
        obj_pk = self.id
        return Comment.objects.filter(content_type=ct, object_pk=obj_pk).count()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self, tags):
        return Tag.objects.get_for_object(self)

    @models.permalink
    def get_absolute_url(self):
        if self.space is not None:
            return ('view-post', (), {
                'space_url': self.space.url,
                'post_id': str(self.id)})
        else:
            return ('view-site-post', (), {
                'post_id': str(self.id)})
