<div id="textfiles" class="container">

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="state" value="list_text">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">

    <div class="list">
	<select name="file" tabindex="1" size="25">
		<?cs each:item = Data.Files ?>
		    <option><?cs var:item ?></option>
		<?cs /each ?>
	</select>
    </div>

    <div class="info">
	<?cs var:Lang.Misc.EditTextInfo ?>
    </div>

    <div class="question">
	<button type="submit" name="action" value="edit_file"><?cs var:Lang.Buttons.EditFile ?></button>
	<button type="submit" name="action" value="cancel"><?cs var:Lang.Buttons.Cancel ?></button>
    </div>

  </form>

</div>
