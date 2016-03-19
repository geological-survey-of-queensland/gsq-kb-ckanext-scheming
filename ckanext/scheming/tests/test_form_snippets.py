from nose.tools import assert_in, assert_not_in
from ckan.lib.base import render_snippet
from jinja2 import Markup

from ckanext.scheming.tests.mock_pylons_request import mock_pylons_request

def render_form_snippet(name, data=None, extra_args=None, **kwargs):
    field = {
        'field_name': 'test',
        'label': 'Test',
    }
    field.update(kwargs)
    with mock_pylons_request():
        return render_snippet(
            'scheming/form_snippets/' + name,
            field=field,
            data=data or {},
            errors=None,
            **(extra_args or {}))

class TestSelectFormSnippet(object):
    def test_choices_visible(self):
        html = render_form_snippet(
            'select.html',
            choices=[{'value': 'one', 'label': 'One'}])
        assert_in('<option value="one">One</option>', html)

    def test_blank_choice_shown(self):
        html = render_form_snippet(
            'select.html',
            choices=[{'value': 'two', 'label': 'Two'}])
        assert_in('<option value="">', html)

    def test_no_blank_choice_on_required(self):
        html = render_form_snippet(
            'select.html',
            choices=[{'value': 'three', 'label': 'Three'}],
            required=True)
        assert_not_in('<option value="">', html)

    def test_blank_choice_shown_on_form_include_blank(self):
        html = render_form_snippet(
            'select.html',
            choices=[{'value': 'four', 'label': 'Four'}],
            required=True,
            form_include_blank_choice=True)
        assert_in('<option value="">', html)

    def test_restrict_choices_to(self):
        html = render_form_snippet(
            'select.html',
            choices=[
                {'value': 'five', 'label': 'Five'},
                {'value': 'six', 'label': 'Six'},
                {'value': 'seven', 'label': 'Seven'}],
            form_restrict_choices_to=['five', 'seven'])
        assert_in('<option value="five">', html)
        assert_not_in('<option value="six">', html)
        assert_in('<option value="seven">', html)

    def test_choice_order_maintained(self):
        html = render_form_snippet(
            'select.html',
            choices=[
                {'value': 'z', 'label': 'Zee'},
                {'value': 'y', 'label': 'Why'},
                {'value': 'x', 'label': 'Ecks'}])
        first, rest = html.split('<option value="z">', 1)
        assert_in('<option value="y">', rest)
        middle, last = rest.split('<option value="y">', 1)
        assert_in('<option value="x">', last)

    def test_choices_sorted_by_label(self):
        html = render_form_snippet(
            'select.html',
            choices=[
                {'value': 'a', 'label': 'Eh'},
                {'value': 'c', 'label': 'Sea'},
                {'value': 'b', 'label': 'Bee'}],
            sorted_choices=True)
        first, rest = html.split('<option value="b">', 1)
        assert_in('<option value="a">', rest)
        middle, last = rest.split('<option value="a">', 1)
        assert_in('<option value="c">', last)


def organization_option_tag(organization, selected_org):
    return Markup('<option value="{orgid}"{selected}>'
        '{display_name}</option>'.format(
        orgid=organization['id'],
        selected=' selected' if selected_org else '',
        display_name=organization['display_name']))


class TestOrganizationFormSnippet(object):
    # It's hard to unit test 'form_snippets/organization.html' because it
    # fetches lists of orgs for the current user, so here we're just testing
    # the org selection part.
    # XXX: Add functional testing in test_form.py to cover that

    def test_organizations_visible(self):
        html = render_form_snippet(
            '_organization_select.html',
            extra_args={
                'organizations_available': [
                    {'id': '1', 'display_name': 'One'}],
                'organization_option_tag': organization_option_tag,
                'org_required': False})
        assert_in('<option value="1">One</option>', html)

    def test_no_organization_shown(self):
        html = render_form_snippet(
            '_organization_select.html',
            extra_args={
                'organizations_available': [
                    {'id': '1', 'display_name': 'One'}],
                'organization_option_tag': organization_option_tag,
                'org_required': False})
        assert_in('<option value="">No organization', html)

    def test_no_organization_hidden_when_required(self):
        html = render_form_snippet(
            '_organization_select.html',
            extra_args={
                'organizations_available': [
                    {'id': '1', 'display_name': 'One'}],
                'organization_option_tag': organization_option_tag,
                'org_required': True})
        assert_not_in('<option value="">', html)

    def test_blank_choice_shown_when_required(self):
        html = render_form_snippet(
            '_organization_select.html',
            form_include_blank_choice=True,
            extra_args={
                'organizations_available': [
                    {'id': '1', 'display_name': 'One'}],
                'organization_option_tag': organization_option_tag,
                'org_required': True})
        assert_in('<option value=""></option>', html)
