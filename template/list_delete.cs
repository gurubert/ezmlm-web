<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ListDelete) ?> &quot;<?cs var:html_escape(Data.List.Name) ?>&quot;</h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ListDelete) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ListDelete) ?> </legend>

	<p><?cs var:Lang.Misc.ConfirmDelete ?></p>
	<form method="post" action="<?cs call:link("","","","","","") ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />

		<input type="hidden" name="action" value="list_delete_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.ConfirmDeletion) ?></button>
	</form>

</fieldset>
