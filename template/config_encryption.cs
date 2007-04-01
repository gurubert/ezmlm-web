<div class="title">
	<h1><?cs var:html_escape(Lang.Title.GnupgOptions) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.GnupgOptions) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.GnupgOptions) ?> </legend>

	<?cs call:form_header("config_encryption", "") ?>
		<input type="hidden" name="config_subset" value="encryption" />

		<?cs call:show_options(UI.Options.Config.GnupgOptions) ?>

		<input type="hidden" name="action" value="config_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button>

	</form>

</fieldset>
