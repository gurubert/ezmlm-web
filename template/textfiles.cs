<div id="textfiles" class="container">

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">

	<ul>
		<?cs if:subcount(Data.List.Files) > 0 ?>
		<!-- scrollbox for list's subscribers -->
		<!-- Keep selection box a reasonable size - suggested by Sebastian Andersson -->
			<?cs if:subcount(Data.List.Files) > 25 ?>
				<?cs set:Data.ScrollSize = 25 ?>
			  <?cs else ?>
				<?cs set:Data.ScrollSize = subcount(Data.List.Files) ?>
			<?cs /if ?>
			<li><select name="file" tabindex="1" size="<?cs var:Data.ScrollSize ?>">
				<?cs each:item = Data.List.Files ?>
					<option><?cs var:item ?></option>
				<?cs /each ?>
			</select></li>
		<?cs else ?>
			<li><?cs var:Lang.Misc.NoFiles ?></li>
		<?cs /if ?>
		
		<li class="info">
			<?cs var:Lang.Misc.EditTextInfo ?>
		</li>

		<button type="submit" name="action" value="textfile_edit"><?cs var:Lang.Buttons.EditFile ?></button>
    </ul>

  </form>

</div>
