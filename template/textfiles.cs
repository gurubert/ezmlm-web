<div class="title">
	<h1><?cs var:html_escape(Lang.Title.FileSelect) ?></h1>
</div>

<div class="introduction">
	<?cs var:html_escape(Lang.Introduction.TextFiles) ?>
</div>

<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.TextFiles) ?> </legend>

<?cs call:form_header("select_textfile") ?>
	<ul>
		<?cs if:subcount(Data.List.CustomizedFiles) +
			subcount(Data.List.DefaultFiles) > 0 ?>
		<!-- scrollbox for list's subscribers -->
		<!-- Keep selection box a reasonable size - suggested by Sebastian Andersson -->
			<?cs if:subcount(Data.List.CustomizedFiles) +
					subcount(Data.List.DefaultFiles) > 15 ?>
				<?cs set:Data.ScrollSize = 15 ?>
			  <?cs else ?>
				<?cs set:Data.ScrollSize = subcount(Data.List.CustomizedFiles) +
					subcount(Data.List.DefaultFiles) ?>
			<?cs /if ?>
			<li><select name="file" size="<?cs var:Data.ScrollSize ?>" style="padding-right:10px">
				<?cs if:subcount(Data.List.CustomizedFiles) > 0 ?>
					<!-- no optgroup if there is no alternative optgroup -->
					<?cs if:subcount(Data.List.DefaultFiles) > 0 ?>
						<optgroup label="<?cs var:html_escape(Lang.Misc.CustomizedFiles) ?>">
						<?cs /if ?>
					<?cs each:item = Data.List.CustomizedFiles ?>
						<option><?cs var:item ?></option>
						<?cs /each ?>
					<?cs if:subcount(Data.List.DefaultFiles) > 0 ?>
						</optgroup>
						<?cs /if ?>
				<?cs /if ?>
				<?cs if:subcount(Data.List.DefaultFiles) > 0 ?>
					<!-- no optgroup if there is no alternative optgroup -->
					<?cs if:subcount(Data.List.CustomizedFiles) > 0 ?>
						<optgroup label="<?cs var:html_escape(Lang.Misc.DefaultFiles) ?>">
						<?cs /if ?>
					<?cs each:item = Data.List.DefaultFiles ?>
						<option><?cs var:item ?></option>
						<?cs /each ?>
					<?cs if:subcount(Data.List.CustomizedFiles) > 0 ?>
						</optgroup>
						<?cs /if ?>
				<?cs /if ?>
			</select></li>
		<?cs else ?>
			<li><?cs var:html_escape(Lang.Misc.NoFiles) ?></li>
		<?cs /if ?>

		<li><input type="hidden" name="action" value="textfile_edit" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.EditFile) ?></button></li>
    </ul>

</form>
</fieldset>

