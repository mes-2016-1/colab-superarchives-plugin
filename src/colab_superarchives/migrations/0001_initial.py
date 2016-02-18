# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hitcounter.models
from django.conf import settings
from django.db import connections
import taggit.managers



sqlmigrate = \
   """
BEGIN;
CREATE TABLE IF NOT EXISTS super_archives_emailaddress (id INTEGER, address INTEGER, real_name INTEGER, md5 INTEGER, user_id INTEGER);
insert into accounts_emailaddress select id, address, real_name, md5, user_id from super_archives_emailaddress 
        where not exists(select id from accounts_emailaddress);
CREATE TABLE IF NOT EXISTS super_archives_emailaddressvalidation (id INTEGER, address INTEGER, validation_key timestamp, created timestamp, user_id INTEGER);
insert into accounts_emailaddressvalidation select id, address, validation_key, created, user_id from super_archives_emailaddressvalidation
        where not exists(select id from accounts_emailaddressvalidation);
CREATE TABLE IF NOT EXISTS super_archives_keyword (id INTEGER, keyword INTEGER, weight INTEGER, thread_id INTEGER);
insert into colab_superarchives_keyword select id, keyword, weight, thread_id from super_archives_keyword
        where not exists(select id from colab_superarchives_keyword);
CREATE TABLE IF NOT EXISTS super_archives_mailinglist (id INTEGER, name INTEGER, email INTEGER, description INTEGER, logo INTEGER, last_imported_index INTEGER, is_private BOOLEAN);
insert into colab_superarchives_mailinglist select id, name, email, description, logo, last_imported_index, is_private
        from super_archives_mailinglist
        where not exists(select id from colab_superarchives_mailinglist);
CREATE TABLE IF NOT EXISTS super_archives_mailinglistmembership (id INTEGER, mailinglist_id INTEGER, user_id INTEGER);
insert into colab_superarchives_mailinglistmembership select id, mailinglist_id, user_id from super_archives_mailinglistmembership
        where not exists(select id from colab_superarchives_mailinglistmembership);
CREATE TABLE IF NOT EXISTS super_archives_message (id INTEGER, subject INTEGER, subject_clean INTEGER, body INTEGER, received_time timestamp, message_id INTEGER, spam BOOLEAN, from_address_id INTEGER, thread_id INTEGER);
insert into colab_superarchives_message select id, subject, subject_clean, body, received_time, message_id, spam, from_address_id, thread_id from super_archives_message
        where not exists(select id from colab_superarchives_message);
CREATE TABLE IF NOT EXISTS super_archives_messageblock (id INTEGER, text INTEGER, is_reply BOOLEAN, "order" INTEGER, message_id INTEGER);
insert into colab_superarchives_messageblock select id, text, is_reply, "order", message_id from super_archives_messageblock
        where not exists(select id from colab_superarchives_messageblock);
CREATE TABLE IF NOT EXISTS super_archives_messagemetadata (id INTEGER, name INTEGER, value INTEGER, "Message_id" INTEGER);
insert into colab_superarchives_messagemetadata select id, name, value, "Message_id" from super_archives_messagemetadata
        where not exists(select id from colab_superarchives_messagemetadata);
CREATE TABLE IF NOT EXISTS super_archives_thread (id INTEGER, subject_token BOOLEAN, score INTEGER, spam BOOLEAN, latest_message_id INTEGER, mailinglist_id INTEGER);
insert into colab_superarchives_thread select id, subject_token, score, spam, latest_message_id, mailinglist_id from super_archives_thread
        where not exists(select id from colab_superarchives_thread);
CREATE TABLE IF NOT EXISTS super_archives_vote (id INTEGER, created timestamp, message_id INTEGER, user_id INTEGER);
insert into colab_superarchives_vote select id, created, message_id, user_id from super_archives_vote
        where not exists(select id from colab_superarchives_vote);

DROP TABLE super_archives_vote CASCADE;
DROP TABLE super_archives_keyword CASCADE;
DROP TABLE super_archives_message CASCADE;
DROP TABLE super_archives_thread CASCADE;
DROP TABLE super_archives_emailaddress CASCADE;
DROP TABLE super_archives_emailaddressvalidation CASCADE;
DROP TABLE super_archives_mailinglistmembership CASCADE;
DROP TABLE super_archives_mailinglist CASCADE;
DROP TABLE super_archives_messageblock CASCADE;
DROP TABLE super_archives_messagemetadata CASCADE;
END;
    """

def runSql(app_name, schema_editor):
    connection = connections['default']
    cursor = connection.cursor()
    # sqlite only allow a single query per execute, so split and execute them.
    if connection.vendor == 'sqlite':
        # remove transaction from the sql string
        listCommands = sqlmigrate.split(';')[1:-2];
        for command in listCommands:
            # sqlite does not accept CASCADE drop
            if 'CASCADE' in command:
                command = command.replace('CASCADE', '')
            cursor.execute(command)
    else:
        cursor.execute(sqlmigrate)

    cursor.close()


def reverseSql(app_name, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0007_auto_20151105_0120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=b'128')),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('?',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=75)),
                ('description', models.TextField()),
                ('logo', models.FileField(upload_to=b'list_logo')),
                ('last_imported_index', models.IntegerField(default=0)),
                ('is_private', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailingListMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mailinglist', models.ForeignKey(to='colab_superarchives.MailingList')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(help_text='Please enter a message subject', max_length=512, verbose_name='Subject', db_index=True)),
                ('subject_clean', models.CharField(max_length=512, db_index=True)),
                ('body', models.TextField(default=b'', help_text='Please enter a message body', verbose_name='Message body')),
                ('received_time', models.DateTimeField(db_index=True)),
                ('message_id', models.CharField(max_length=512)),
                ('spam', models.BooleanField(default=False)),
                ('from_address', models.ForeignKey(to='accounts.EmailAddress')),
            ],
            options={
                'ordering': ('received_time',),
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('is_reply', models.BooleanField(default=False)),
                ('order', models.IntegerField()),
                ('message', models.ForeignKey(related_name='blocks', to='colab_superarchives.Message')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('value', models.TextField()),
                ('Message', models.ForeignKey(to='colab_superarchives.Message')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject_token', models.CharField(max_length=512)),
                ('score', models.IntegerField(default=0, help_text='Thread score', verbose_name='Score')),
                ('spam', models.BooleanField(default=False)),
                ('latest_message', models.OneToOneField(related_name='+', null=True, to='colab_superarchives.Message', help_text='Latest message posted', verbose_name='Latest message')),
                ('mailinglist', models.ForeignKey(verbose_name='Mailing List', to='colab_superarchives.MailingList', help_text='The Mailing List where is the thread')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ('-latest_message__received_time',),
                'verbose_name': 'Thread',
                'verbose_name_plural': 'Threads',
            },
            bases=(models.Model, hitcounter.models.HitCounterModelMixin),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(to='colab_superarchives.Message')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'message')]),
        ),
        migrations.AlterUniqueTogether(
            name='thread',
            unique_together=set([('subject_token', 'mailinglist')]),
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(to='colab_superarchives.Thread', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='message',
            unique_together=set([('thread', 'message_id')]),
        ),
        migrations.AddField(
            model_name='keyword',
            name='thread',
            field=models.ForeignKey(to='colab_superarchives.Thread'),
            preserve_default=True,
        ),
        migrations.RunPython(runSql, reverseSql),
    ]
