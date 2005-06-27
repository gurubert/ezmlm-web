<div id="textfiles" class="container">

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
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
	<button type="submit" name="action" value="edit_file_ask"><?cs var:Lang.Buttons.EditFile ?></button>
    </div>

  </form>

</div>
