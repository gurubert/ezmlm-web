<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigArchive) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigArchive) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ConfigArchive) ?> </legend>

	<?cs call:form_header("config_archive", "") ?>
		<input type="hidden" name="config_subset" value="archive" />

		<?cs call:show_options(UI.Options.Config.Archive) ?>

		<input type="hidden" name="action" value="config_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button>

	</form>
</fieldset>

