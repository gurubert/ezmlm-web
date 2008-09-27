<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<?cs var:html_escape(Lang.Misc.MimeReject) ?>:
<ul>
	<li><textarea name="mimereject" rows="4" cols="60"><?cs
		var:html_escape(Data.List.MimeReject) ?></textarea>
	</li>
</ul>
