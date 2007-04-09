<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ListCreate) ?></h1>
</div>

<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.ListCreate) ?> </legend>

	<?cs call:form_header("list_create", "") ?>
		
		<?cs call:show_options(UI.Options.Create) ?>

		<input type="hidden" name="action" value="list_create_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.Create) ?></button>
	</form>

</fieldset>

