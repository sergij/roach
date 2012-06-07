# coding: utf-8
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
from django.forms.util import flatatt

AC_MODEL_CHOICE_TEMPLATE = u'''
<span>
    <input type="hidden" name="%(name)s" id="id_hidden_%(name)s" value="%(hidden_value)s" />
    <input type="text" id="id_%(name)s" value="%(value)s" data-old-value="%(value)s" %(attrs)s />
    <script type="text/javascript">
        var chainedParams = {}
        if ('%(chained_to)s') {
            chainedParams = {
                '%(chained_to)s': function () {return $('input[name=%(chained_to)s]').val()}
            }
        }
        $('#id_%(name)s').autocomplete('%(ac_url)s', {
            extraParams: chainedParams
        }).result(function(event, item){
            if(item[1]) {
                // сохраняем значение поля, чтобы вычислять актульность id
                $(this).data('old-value', item[0])
                $('#id_hidden_%(name)s').val(item[1])
            }
        }).change(function(){
            var $this = $(this)
            if ($this.val() != $this.data('old-value')) {
                // сброс заполненного id при изменении
                $('#id_hidden_%(name)s').val('')
            }
        })
    </script>
</span>
'''

class AutoModelChoiceWidget(widgets.Widget):

    AC_TEMPLATE = AC_MODEL_CHOICE_TEMPLATE

    def __init__(self, ac_view_name, chain_queryset, choice_field='pk', chained_to=None, attrs=None):
        super(AutoModelChoiceWidget, self).__init__(attrs)
        self.ac_view_name = ac_view_name
        self.choices = []
        self.chained_to = chained_to or u''
        self.choice_field = choice_field
        self.chain_queryset = chain_queryset

    def get_name(self, selected_value):
        try:
            return self.chain_queryset.get(**dict([(self.choice_field, selected_value)]))
        except (self.chain_queryset.model.DoesNotExist, ValueError):
            return u''

    def render(self, name, value, attrs=None):
        ac_url = reverse(self.ac_view_name)
        chained_to = self.chained_to

        if not value:
            value = hidden_value = u''
        else:
            value = force_unicode(value)
            hidden_value = value
            value = self.get_name(value)

        attrs = flatatt(self.build_attrs(attrs))
        return mark_safe(self.AC_TEMPLATE % {
            'ac_url': ac_url,
            'name': name,
            'value': value,
            'hidden_value': hidden_value,
            'attrs': attrs,
            'chained_to': chained_to,
        })
