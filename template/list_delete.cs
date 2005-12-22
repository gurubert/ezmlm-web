<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfirmDelete) ?> <i><?cs var:html_escape(Data.List.Name) ?></i></h1>
</div>

<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />
	<?cs if:Data.List.PartType ?>
		<input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>" />
	<?cs /if?>

	<input type="hidden" name="action" value="list_delete_do" />
	<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.ConfirmDeletion) ?></button>
</form>

