<label for="listaddress"><?cs var:html_escape(Lang.Misc.ListAddress) ?>:</label>
	<input type="text" id="listaddress" name="inlocal" size="20"
		value="<?cs var:html_escape(Data.LocalPrefix)
		?>"> @ <input type="text" name="inhost" size="30" value="<?cs
		var:html_escape(Data.HostName) ?>"></li>
