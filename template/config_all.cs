<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigAll) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigAll) ?></p>
</div>

<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.ConfigAll) ?> </legend>

	<?cs call:form_header("config_all", "") ?>
		<input type="hidden" name="config_subset" value="all" />

		<?cs call:show_options(UI.Options.Config.Overview) ?>

		<input type="hidden" name="action" value="config_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button>

	</form>
</fieldset>

