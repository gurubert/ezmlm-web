<div class="title">
	<h1><?cs var:html_escape(Lang.Title.FileSelect) ?></h1>
</div>

<div class="introduction">
	<?cs var:html_escape(Lang.Introduction.TextFiles) ?>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.TextFiles) ?> </legend>

<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />

	<ul>
		<?cs if:subcount(Data.List.Files) > 0 ?>
		<!-- scrollbox for list's subscribers -->
		<!-- Keep selection box a reasonable size - suggested by Sebastian Andersson -->
			<?cs if:subcount(Data.List.Files) > 15 ?>
				<?cs set:Data.ScrollSize = 15 ?>
			  <?cs else ?>
				<?cs set:Data.ScrollSize = subcount(Data.List.Files) ?>
			<?cs /if ?>
			<li><select name="file" size="<?cs var:Data.ScrollSize ?>">
				<?cs each:item = Data.List.Files ?>
					<option><?cs var:item ?></option>
				<?cs /each ?>
			</select></li>
		<?cs else ?>
			<li><?cs var:html_escape(Lang.Misc.NoFiles) ?></li>
		<?cs /if ?>

		<li><input type="hidden" name="action" value="textfile_edit" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.EditFile) ?></button></li>
    </ul>

</form>
</fieldset>

