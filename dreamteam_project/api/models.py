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


class Member(AbstractUser):
    position = models.CharField(_('Position'), max_length=3, choices=MemberPosition.choices)
    is_manager = models.BooleanField(default=False)

    class Meta:
        db_table = 'members'
        verbose_name = _('member')
        verbose_name_plural = _('all members')
        ordering = ['username']

    def __str__(self):
        return self.username


class Team(models.Model):
    name = models.CharField(_('Team Name'), max_length=40)
    members = models.ManyToManyField(Member, through='TeamMembership')

    class Meta:
        db_table = 'teams'
        verbose_name = _('team')
        verbose_name_plural = _('all teams')
        ordering = ['name']

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'team_memberships'
