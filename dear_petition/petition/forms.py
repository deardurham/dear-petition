import tempfile

from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(label="CIRPS Detail Report")

    def save(self):
        file_ = self.cleaned_data['file']
        with tempfile.TemporaryFile() as fp:
            fp.write(file_.read())
            import ipdb; ipdb.set_trace()
            print(file_)
