<div class="title">
	<h1><?cs var:Lang.Title.SelectFile ?></h1>
</div>

<div class="introduction">
	<?cs var:Lang.Introduction.EditTextFile ?>
</div>

<fieldset class="form">
	<legend><?cs var:Lang.Legend.TextFiles ?></legend>

<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">

	<ul>
		<?cs if:subcount(Data.List.Files) > 0 ?>
		<!-- scrollbox for list's subscribers -->
		<!-- Keep selection box a reasonable size - suggested by Sebastian Andersson -->
			<?cs if:subcount(Data.List.Files) > 15 ?>
				<?cs set:Data.ScrollSize = 15 ?>
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

		<button type="submit" name="action" value="textfile_edit"><?cs var:Lang.Buttons.EditFile ?></button>
    </ul>

</form>
</fieldset>

