<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- headerfilter -->
<?cs if:Config.Features.KeepFiles ?>
	<?cs var:html_escape(Lang.Misc.HeaderFiltering) ?>:
	<ul>
	<li><input type="radio" name="headerfilter_action" value="remove"
		id="hf_remove"<?cs if:Data.List.HeaderRemove
			?> checked="checked"<?cs /if ?> /><label for="hf_remove"><?cs
			var:html_escape(Lang.Misc.HeaderRemove) ?></label></li>
	<li><input type="radio" name="headerfilter_action" value="keep"
		id="hf_keep"<?cs if:Data.List.HeaderKeep
			?> checked="checked"<?cs /if ?> /><label for="hf_keep"><?cs
			var:html_escape(Lang.Misc.HeaderKeep) ?></label></li>
	<li>
		<textarea name="headerfilter" rows="5" cols="70"><?cs
			if Data.List.HeaderRemove ?><?cs
			var:html_escape(Data.List.HeaderRemove) ?><?cs else ?><?cs
			var:html_escape(Data.List.HeaderKeep) ?><?cs /if ?></textarea></li>
	</ul>
<?cs else ?>
	<?cs var:html_escape(Lang.Misc.HeaderFiltering) ?>:
	<?cs var:html_escape(Lang.Misc.HeaderRemove) ?>
	<input type="hidden" name="headerfilter_action" value="remove" />
	<ul>
	<li>
		<textarea name="headerfilter" rows="5" cols="70"><?cs
			if Data.List.HeaderRemove ?><?cs
			var:html_escape(Data.List.HeaderRemove) ?><?cs else ?><?cs
			var:html_escape(Data.List.HeaderKeep) ?><?cs /if ?></textarea></li>
	</ul>
<?cs /if ?>
