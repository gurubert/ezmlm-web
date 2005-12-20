<div id="edittext" class="container">

    <div class="title">
	<h2><?cs var:Lang.Misc.EditingFile ?> &quot;<?cs var:Data.List.File.Name ?>&quot;</h2>
    </div>

    <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
	<input type="hidden" name="file" value="<?cs var:Data.List.File.Name ?>">
	
	<div class="input">
	    <span class="formfield"><textarea name="content"
	      rows="20" cols="72"><?cs var:Data.List.File.Content ?></textarea></span>
	</div>

	<div class="info">
	    <?cs var:Lang.Misc.EditFileInfo ?>
	</div>

    <button type="submit" name="action" value="textfile_save"><?cs var:Lang.Buttons.SaveFile ?></button>

    </form>

</div>
