import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .validators import validate_i18nJSON


def get_choicesets_enum(className):
    class_vars = vars(className)
    choicesets = []
    for i in class_vars:
        if type(class_vars[i]) == models.enums.ChoicesMeta:
            choicesets.append(
                {i: [x for x in class_vars[i]._member_names_ if x[0] != "_"]}
            )
    return choicesets


class i18nJSONField(models.JSONField):
    default_validators = [validate_i18nJSON]


class BaseModel(models.Model):
    """BaseModel

    Defines the following fields

        id:UUID
        created_on:DateTime
        edited_on:DateTime
        _data:JSON(null&blank allowed)

    And the following class methods

        get_choicesets()->dict
            returns all choicefields and their choices
        get_fields()->list
            returns all fields defined in the model
        get_related_fields()->list
            returns all _set fields aka forward references
        get_all_fields()->list
            returns all fields including forward references

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
    _data = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True

    @classmethod
    def get_choicesets(cls) -> dict:
        choicesets = dict()
        for i in cls._meta.fields:
            if i.choices != None:
                choicesets[i.name] = list(dict(i.choices))
            else:
                continue
        return choicesets

    @classmethod
    def get_fields(cls) -> list:
        return [x.name for x in cls._meta.fields]

    @classmethod
    def get_related_fields(cls) -> list:
        return [x.name for x in cls._meta.related_objects] + [
            x.name for x in cls._meta.many_to_many
        ]

    @classmethod
    def get_many_to_many_fields(cls) -> list:
        return [x.name for x in cls._meta.many_to_many]

    @classmethod
    def get_all_fields(cls) -> list:
        return (
            [x.name for x in cls._meta.fields]
            + [x.name for x in cls._meta.related_objects]
            + [x.name for x in cls._meta.many_to_many]
        )

    @classmethod
    def get_all_fields_verbose(cls) -> list:
        return (
            [x.verbose_name for x in cls._meta.fields]
            + [x.verbose_name for x in cls._meta.related_objects]
            + [x.verbose_name for x in cls._meta.many_to_many]
        )

    @classmethod
    def generate_i18nJSON(cls, lang_codes):
        i18nFields = ["id"] + [
            x.name for x in cls._meta.fields if type(x) == i18nJSONField
        ]
        i18nTexts = cls.objects.values_list(*i18nFields)
        i18nTextGroups = dict()
        for texts in i18nTexts:
            for i in range(len(i18nFields)):
                if i18nFields[i] not in i18nTextGroups:
                    i18nTextGroups[i18nFields[i]] = []
                i18nTextGroups[i18nFields[i]].append(texts[i])
        i18nJSON = dict()
        for lang in lang_codes:
            i18nJSON[lang] = dict()
            i18nJSON[lang][cls.__name__] = dict()
            for i in range(len(i18nTextGroups["id"])):
                i18nJSON[lang][cls.__name__][str(
                    i18nTextGroups["id"][i])] = dict()
                for field in i18nFields[1:]:
                    if i18nTextGroups[field][i]:
                        i18nJSON[lang][cls.__name__][str(i18nTextGroups["id"][i])][
                            field
                        ] = i18nTextGroups[field][i][lang]
                    else:
                        i18nJSON[lang][cls.__name__][str(i18nTextGroups["id"][i])][
                            field
                        ] = None
        return i18nJSON

    @classmethod
    def get_all_search_fields(cls) -> list:
        search_fields = list()
        for field in cls._meta.fields:
            if field.is_relation:
                for field_relation in cls._meta.get_field(field.name).remote_field.model._meta.fields:
                    if not field_relation.is_relation and field_relation.name not in ['id', 'created_on', 'edited_on', '_data']:
                        search_fields.append(
                            f'{field.name}__{field_relation.name}')
            else:
                search_fields.append(field.name)
        return search_fields


class AbstractBaseUser(BaseModel, AbstractUser):
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    full_name = models.CharField(max_length=1024, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    class Meta:
        abstract = True
