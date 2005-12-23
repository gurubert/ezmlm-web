<div class="title">
	<h1><?cs var:html_escape(Lang.Title.FileEdit) ?> &quot;<?cs var:Data.List.File.Name ?>&quot;</h1>
</div>

<div class="introduction">
	<?cs var:html_escape(Lang.Introduction.EditTextFile) ?>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.TextFileEdit) ?> </legend>

<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
	<input type="hidden" name="file" value="<?cs var:Data.List.File.Name ?>">
	
	<p><textarea name="content" rows="13"
			cols="72"><?cs var:Data.List.File.Content ?></textarea></p>

    <input type="hidden" name="action" value="textfile_save" />
    <button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.SaveFile) ?></button>
</form>

</fieldset>

<?cs include:TemplateDir + '/help_tag_substitution.cs' ?>
