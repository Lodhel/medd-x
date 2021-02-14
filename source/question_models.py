from django.db import models
from django.contrib.postgres.fields import ArrayField


class QuestionBlock(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    question_list = ArrayField(models.IntegerField(), null=True)
    question_group_list = ArrayField(models.IntegerField(), null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'question_block'


class QuestionGroup(models.Model):
    question_list = ArrayField(models.IntegerField())

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'question_group'


class Question(models.Model):
    author = models.IntegerField()
    role_of_author = models.CharField(default="anonym", max_length=256)

    STATUS_TYPES = (
        ('public', 'public'),
        ('custom', 'custom'),
        ('draft', 'draft')
    )
    status = models.CharField(choices=STATUS_TYPES, max_length=256)

    QUESTION_TYPES = (
        ('table', 'table'),
        ('upload_link', 'upload_link'),
        ('upload_file', 'upload_file'),
        ('select_list', 'select_list'),
        ('date', 'date'),
        ('text', 'text'),
        ('numeric_with_measurement_unit', 'numeric_with_measurement_unit'),
        ('numeric', 'numeric'),
        ('toggle', 'toggle'),
    )
    question_type = models.CharField(choices=QUESTION_TYPES, max_length=256)

    DATA_TYPES = (
        ('medical', 'medical'),
        ('non-medical', 'non-medical'),
        ('clarifying', 'clarifying')
    )
    data_type = models.CharField(choices=DATA_TYPES, max_length=256)
    question_value = models.TextField()
    question_label = models.TextField(null=True, blank=True)
    prompt_text = models.TextField(null=True, blank=True)
    required_answer = models.BooleanField(default=False)
    allow_multiple_answer = models.BooleanField(default=False)
    historically_tracked = models.BooleanField(default=False)
    parent_question_id = models.IntegerField(null=True, blank=True)  # only clarifying
    answer_values = ArrayField(models.CharField(max_length=128), null=True, blank=True)  # only toggle
    multiple_selection = models.BooleanField(default=False)  # only select_list
    min_additions = models.IntegerField(null=True, blank=True)  # only upload file/link
    max_additions = models.IntegerField(null=True, blank=True)  # only upload file/link
    min_symbols = models.IntegerField(null=True, blank=True)  # only text
    max_symbols = models.IntegerField(null=True, blank=True)  # only text
    rows_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6')
    )
    rows_number = models.CharField(choices=rows_choices, default="2", max_length=256)  # only text
    keywords_recognize = models.BooleanField(default=False)  # only text
    date_type = models.CharField(choices=(('one', 'one'), ("start_and_end", "start_and_end")), null=True, max_length=256)  # only date
    allow_current_future_date = models.BooleanField(default=False)  # only date
    allow_approximate_date = models.BooleanField(default=False)  # only date
    measurement_units = models.CharField(max_length=128, null=True, blank=True)  # numeric with Measurement
    measurement_unit_by_default = models.CharField(null=True, max_length=256, blank=True)  # numeric with Measurement
    attachment_choices = (
        ('')
    )
    attachment_formats = models.CharField(max_length=128, choices=attachment_choices, null=True, blank=True)  # only upload_file {selectlist with formats}/{not define}
    created_table = models.IntegerField(null=True, blank=True)  # only table
    refbook_for_selectlist = models.IntegerField(null=True, blank=True)  # only rb
    allow_other = models.BooleanField(default=False)  # only rb

    meddata_types = (
        ('Condition or Disease', 'Condition or Disease'),
        ('Symptom', 'Symptom'),
        ('Human parameter', 'Human parameter'),
        ('Lifestyle and habits', 'Lifestyle and habits'),
        ('Diet and nutrition', 'Diet and nutrition'),
        ('Environment Influence', 'Environment Influence'),
        ('Anamnesis and Chronic', 'Anamnesis and Chronic'),
        ('Procedure or Exam', 'Procedure or Exam'),
        ('Genetic heredity', 'Genetic heredity'),
        ('Laboratory test', 'Laboratory test'),
        ('Treatment', 'Treatment'),
        ('Allergy or Asthma', 'Allergy or Asthma'),
        ('Additional information', 'Additional information'),
        ('Cause of pathology', 'Cause of pathology')
    )
    meddata_type = models.CharField(choices=meddata_types, null=True, blank=True)
    biomarket_choicee = ()
    biomarket = models.CharField(choices=meddata_types, null=True, blank=True)
    answer_impact_to_health_status = models.CharField()
    influence_to_additional_question = models.TextField(null=True, blank=True)
    default_chapter = models.CharField()
    default_block = models.CharField()
    destination_chapters = models.CharField()
    destination_blocks = models.CharField()
    age_groups = models.CharField()
    gender = models.CharField(max_length=64, choices=(('male', 'male'), ('female', 'female')), default='male')
    comment = models.TextField(null=True, blank=True)
    notification = models.TextField(null=True, blank=True)
    additional_questions = ArrayField(models.IntegerField(), blank=True, null=True)
    divider = models.BooleanField(default=False)

    def __str__(self):
        return self.question_value

    class Meta:
        db_table = 'question'


class ChoiceMeasurment(models.Model):
    title = models.CharField(max_length=4096)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'choice_measurment'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'answer'


class Chapter(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    question_list = ArrayField(models.IntegerField(), null=True)
    question_group_list = ArrayField(models.IntegerField(), null=True)
    question_block_list = ArrayField(models.IntegerField(), null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'chapter'


class Questionnarie(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    question_list = ArrayField(models.IntegerField(), null=True)
    question_group_list = ArrayField(models.IntegerField(), null=True)
    question_block_list = ArrayField(models.IntegerField(), null=True)
    chapter_list = ArrayField(models.IntegerField(), null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'questionnarie'