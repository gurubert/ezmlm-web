<div id="edittext" class="container">

    <div class="title">
	<h2><?cs var:Lang.Misc.EditingFile ?> <?cs var:Data.File.Name ?></h2>
    </div>

    <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
	<input type="hidden" name="file" value="<?cs var:Data.File.Name ?>">
	
	<div class="input">
	    <span class="formfield"><textarea name="content"
	      rows="20" cols="72"><?cs var:Data.File.Content ?></textarea></span>
	</div>

	<div class="info">
	    <?cs var:Lang.Misc.EditFileInfo ?>
	</div>

	<div class="question">
	    <button type="submit" name="action" value="edit_text_do"><?cs var:Lang.Buttons.SaveFile ?></button>
	    <button type="reset" name="action" value="reset"><?cs var:Lang.Buttons.ResetForm ?></button>
	</div>

    </form>

</div>
