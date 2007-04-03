<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<?cs if:Config.Features.KeepFiles ?>
	<?cs var:html_escape(Lang.Misc.MimeFiltering) ?>:
	<ul>
	<li><input type="radio" name="mimefilter_action" value="remove"
		id="mf_remove"<?cs if:Data.List.MimeRemove
			?> checked="checked"<?cs /if ?> /><label for="mf_remove"><?cs
			var:html_escape(Lang.Misc.MimeRemove) ?></label></li>
	<li><input type="radio" name="mimefilter_action" value="keep"
		id="mf_keep"<?cs if:Data.List.MimeKeep
			?> checked="checked"<?cs /if ?> /><label for="mf_keep"><?cs
			var:html_escape(Lang.Misc.MimeKeep) ?></label></li>
	<li>
		<textarea name="mimefilter" rows="5" cols="70"><?cs
			if Data.List.MimeRemove ?><?cs var:html_escape(Data.List.MimeRemove)
			?><?cs else ?><?cs var:html_escape(Data.List.MimeKeep)
			?><?cs /if ?></textarea></li>
		<li>(<a href="<?cs call:link('action','show_mime_examples','','','','')
			?>" target="_blank"><?cs var:html_escape(Lang.Misc.MimeTypeExamples)
			?></a>)</li>
	</ul>
<?cs else ?>
	<?cs var:html_escape(Lang.Misc.MimeFiltering) ?>:
	<?cs var:html_escape(Lang.Misc.MimeRemove) ?>
	<input type="hidden" name="mimefilter_action" value="remove" />
	<ul><li>
		<textarea name="mimefilter" rows="5" cols="70"><?cs
			if Data.List.MimeRemove ?><?cs var:html_escape(Data.List.MimeRemove)
			?><?cs else ?><?cs var:html_escape(Data.List.MimeKeep)
			?><?cs /if ?></textarea></li>
	</ul>
<?cs /if ?>
<?cs # uncomment the following to enable the 'reset' feature
	but that would mess up the interface, right? ?>
<?cs # call:checkbox("x") ?>
