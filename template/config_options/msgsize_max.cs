<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- message size limit -->
<input type="checkbox" name="msgsize_max_state"
	value="selected" id="msgsize_max_state" <?cs
	if:Data.List.MsgSize.Max>0 ?>checked="checked"<?cs /if ?> />
	<label for="msgsize_max_state"><?cs var:html_escape(Lang.Misc.MessageSize.Max) ?></label>
	<ul><li><input type="text" name="msgsize_max_value" size="10"
	style="text-align:right" value="<?cs
	alt:Data.List.MsgSize.Max ?>30000<?cs /alt ?>" /> <?cs
	var:html_escape(Lang.Misc.MessageSize.Unit) ?></li></ul>
