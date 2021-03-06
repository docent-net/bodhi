import re

import colander

from kitchen.iterutils import iterate

from bodhi.models import (UpdateRequest, UpdateSeverity, UpdateStatus,
                          UpdateSuggestion, UpdateType)


CVE_REGEX = re.compile(r"CVE-[0-9]{4,4}-[0-9]{4,}")


def splitter(value):
    """Parse a string or list of comma or space delimited builds"""
    if value == colander.null:
        return

    items = []
    for v in iterate(value):
        if isinstance(v, basestring):
            for item in v.replace(',', ' ').split():
                items.append(item)

        elif v is not None:
            items.append(v)

    return items


class Bugs(colander.SequenceSchema):
    bug = colander.SchemaNode(colander.Integer(), missing=None)


class Builds(colander.SequenceSchema):
    build = colander.SchemaNode(colander.String())


class CVE(colander.String):
    def deserialize(self, node, cstruct):
        value = super(CVE, self).deserialize(node, cstruct)

        if CVE_REGEX.match(value) is None:
            raise colander.Invalid(node, '"%s" is not a valid CVE id' % value)

        return value


class CVEs(colander.SequenceSchema):
    cve = colander.SchemaNode(CVE())


class Packages(colander.SequenceSchema):
    package = colander.SchemaNode(colander.String())


class Releases(colander.SequenceSchema):
    release = colander.SchemaNode(colander.String())


class SaveUpdateSchema(colander.MappingSchema):
    builds = Builds(colander.Sequence(accept_scalar=True),
                    preparer=[splitter])

    bugs = Bugs(colander.Sequence(accept_scalar=True),
                preparer=[splitter])

    close_bugs = colander.SchemaNode(
        colander.Boolean(),
        missing=True,
    )
    type = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(UpdateType.values()),
    )
    request = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(UpdateRequest.values()),
        missing='testing',
    )
    severity = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(UpdateSeverity.values()),
        missing='unspecified',
    )
    notes = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=10),
    )
    autokarma = colander.SchemaNode(
        colander.Boolean(),
        missing=True,
    )
    stable_karma = colander.SchemaNode(
        colander.Integer(),
        validator=colander.Range(min=1),
        missing=3,
    )
    unstable_karma = colander.SchemaNode(
        colander.Integer(),
        validator=colander.Range(max=-1),
        missing=-3,
    )
    suggest = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(UpdateSuggestion.values()),
        missing='unspecified',
    )
    edited = colander.SchemaNode(
        colander.String(),
        missing='',
    )


class ListUpdateSchema(colander.MappingSchema):
    approved_since = colander.SchemaNode(
        colander.DateTime(),
        location="querystring",
        missing=None,
    )

    bugs = Bugs(
        colander.Sequence(accept_scalar=True),
        location="querystring",
        missing=None,
        preparer=[splitter],
    )

    critpath = colander.SchemaNode(
        colander.Boolean(true_choices=('true', '1')),
        location="querystring",
        missing=None,
    )

    cves = CVEs(
        colander.Sequence(accept_scalar=True),
        location="querystring",
        missing=None,
        preparer=[splitter],
    )

    locked = colander.SchemaNode(
        colander.Boolean(true_choices=('true', '1')),
        location="querystring",
        missing=None,
    )

    modified_since = colander.SchemaNode(
        colander.DateTime(),
        location="querystring",
        missing=None,
    )

    packages = Packages(
        colander.Sequence(accept_scalar=True),
        location="querystring",
        missing=None,
        preparer=[splitter],
    )

    pushed = colander.SchemaNode(
        colander.Boolean(true_choices=('true', '1')),
        location="querystring",
        missing=None,
    )

    pushed_since = colander.SchemaNode(
        colander.DateTime(),
        location="querystring",
        missing=None,
    )

    qa_approved = colander.SchemaNode(
        colander.Boolean(true_choices=('true', '1')),
        location="querystring",
        missing=None,
    )

    qa_approved_since = colander.SchemaNode(
        colander.DateTime(),
        location="querystring",
        missing=None,
    )

    releases = Releases(
        colander.Sequence(accept_scalar=True),
        location="querystring",
        missing=None,
        preparer=[splitter],
    )

    releng_approved = colander.SchemaNode(
        colander.Boolean(true_choices=('true', '1')),
        location="querystring",
        missing=None,
    )

    releng_approved_since = colander.SchemaNode(
        colander.DateTime(),
        location="querystring",
        missing=None,
    )

    request = colander.SchemaNode(
        colander.String(),
        location="querystring",
        missing=None,
        validator=colander.OneOf(UpdateRequest.values()),
    )

    security_approved = colander.SchemaNode(
        colander.Boolean(true_choices=('true', '1')),
        location="querystring",
        missing=None,
    )

    security_approved_since = colander.SchemaNode(
        colander.DateTime(),
        location="querystring",
        missing=None,
    )

    severity = colander.SchemaNode(
        colander.String(),
        location="querystring",
        missing=None,
        validator=colander.OneOf(UpdateSeverity.values()),
    )

    status = colander.SchemaNode(
        colander.String(),
        location="querystring",
        missing=None,
        validator=colander.OneOf(UpdateStatus.values()),
    )

    submitted_since = colander.SchemaNode(
        colander.DateTime(),
        location="querystring",
        missing=None,
    )

    suggest = colander.SchemaNode(
        colander.String(),
        location="querystring",
        missing=None,
        validator=colander.OneOf(UpdateSuggestion.values()),
    )

    type = colander.SchemaNode(
        colander.String(),
        location="querystring",
        missing=None,
        validator=colander.OneOf(UpdateType.values()),
    )

    user = colander.SchemaNode(
        colander.String(),
        location="querystring",
        missing=None,
    )
