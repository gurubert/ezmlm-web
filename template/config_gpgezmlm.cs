<div class="title">
	<h1><?cs var:html_escape(Lang.Title.GpgEzmlmOptions) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.GpgEzmlmOptions) ?></p>
</div>

<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.GpgEzmlmOptions) ?> </legend>

	<?cs call:form_header("config_gpgezmlm") ?>
		<input type="hidden" name="config_subset" value="gpgezmlm" />

		<?cs call:show_options(UI.Options.Config.GpgEzmlmOptions) ?>

	<ul><li>
		<input type="hidden" name="action" value="config_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button></li></ul>

	</form>

</fieldset>
