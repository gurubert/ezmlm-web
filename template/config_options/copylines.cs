<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- 'copylines' setting -->
<?cs if:Config.Features.CopyLines ?>
	<input type="checkbox" name="copylines_enabled"
			value="selected" id="copylines_enabled" <?cs
			if:Data.List.CopyLines>0 ?>checked="checked"<?cs /if ?> />
			<label for="copylines_enabled"><?cs
			var:html_escape(Lang.Misc.CopyLinesEnabled) ?></label>
		<ul><li><input type="text" name="copylines" size="10"
			style="text-align:right" value="<?cs
			alt:Data.List.CopyLines ?>0<?cs /alt ?>" /> <?cs
			var:html_escape(Lang.Misc.CopyLinesNumber) ?></li></ul>
<?cs /if ?>
