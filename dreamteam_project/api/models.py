from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class MemberPosition(models.TextChoices):
    """
    Enum-like class defines member position.
    """
    INTERN = 'INT', _('Intern')
    JUNIOR = 'JUN', _('Junior')
    MIDDLE = 'MID', _('Middle')
    SENIOR = 'SEN', _('Senior')
    TECH_LEAD = 'TCH', _('Tech Lead')
    TEAM_LEAD = 'TML', _('Team Lead')
    PM = 'PM', _('Project Manager')
    ARCHITECT = 'ARC', _('Architect')
    DBA = 'DBA', _('Database Administrator')
    QA = 'QAE', _('Quality Assurance Engineer')
    DEV = 'DEV', _('DevOps Engineer')
    UI_UX = 'UI', _('UI/UX Designer')
    CEO = 'CEO', _('Chief Executive Officer')

    @classmethod
    def only_one_team(cls):
        return ['INT', 'JUN', 'SEN', 'MID', 'TCH']

    @classmethod
    def allow_manage(cls):
        return ['CEO', 'TML', 'PM']


class Member(AbstractUser):
    email = models.EmailField(_('Email address'), unique=True, blank=True)
    position = models.CharField(_('Position'), max_length=3, choices=MemberPosition.choices)
    is_manager = models.BooleanField(default=False)

    class Meta:
        db_table = 'members'
        verbose_name = _('member')
        verbose_name_plural = _('all members')
        ordering = ['username']

    def save(self, *args, **kwargs):
        """
        Overridden default save method to set ...
        """
        if self.is_superuser or self.position in MemberPosition.allow_manage():
            self.is_manager = True

        if password := self.password:
            self.password = make_password(password)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Team(models.Model):
    name = models.CharField(_('Team Name'), max_length=40, unique=True, db_index=True)
    members = models.ManyToManyField(Member, through='TeamMembership')

    class Meta:
        db_table = 'teams'
        verbose_name = _('team')
        verbose_name_plural = _('all teams')
        ordering = ['name']

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='team_memberships')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='memberships')
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'team_memberships'
        unique_together = ('member', 'team')
