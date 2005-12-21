<div class="title">
	<h1><?cs var:Lang.Misc.ConfirmDelete ?> <i><?cs var:Data.List.Name ?></i></h1>
</div>

<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
	<?cs if:Data.List.PartType ?>
		<input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>">
	<?cs /if?>

	<button type="submit" name="action" tabindex="1" value="list_delete_do"><?cs var:Lang.Buttons.ConfirmDeletion ?></button>
</form>

