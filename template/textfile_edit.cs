<div class="title">
	<h1><?cs var:html_escape(Lang.Title.FileEdit) ?> &quot;<?cs var:Data.List.File.Name ?>&quot;</h1>
</div>

<div class="introduction">
	<?cs var:html_escape(Lang.Introduction.EditTextFile) ?>
</div>


<!-- reset text file -->
<?cs if:(Data.areDefaultTextsAvailable == 1) && (Data.List.File.isDefault == 0) ?>
	<fieldset>
		<legend><?cs var:html_escape(Lang.Legend.TextFileReset) ?> </legend>

		<div class="introduction">
			<?cs var:html_escape(Lang.Introduction.ResetTextFile) ?>
		</div>

	<?cs call:form_header("textfile_reset", "") ?>
		<input type="hidden" name="file" value="<?cs var:Data.List.File.Name ?>">
		<input type="hidden" name="action" value="textfile_reset" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.ResetFile) ?></button>
	</form>
	</fieldset>
<?cs /if ?>

<!-- edit text file -->
<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.TextFileEdit) ?> </legend>

<?cs call:form_header("textfile_reset", "") ?>
	<input type="hidden" name="file" value="<?cs var:Data.List.File.Name ?>">
	
	<p><textarea name="content" rows="13"
			cols="72"><?cs var:html_escape(Data.List.File.Content) ?></textarea></p>

    <input type="hidden" name="action" value="textfile_save" />
    <button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.SaveFile) ?></button>
</form>

</fieldset>

<?cs include:TemplateDir + '/help_tag_substitution.cs' ?>
