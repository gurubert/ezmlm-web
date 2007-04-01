<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigMain) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigMain) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ConfigMain) ?> </legend>

	<?cs call:form_header("config_main", "") ?>
		<input type="hidden" name="config_subset" value="main" />

		<?cs call:show_options(UI.Options.Config.Main) ?>

		<input type="hidden" name="action" value="config_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button>

	</form>

</fieldset>
