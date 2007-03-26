<?cs if:Data.List.Features.Crypto ?>
<!-- expiration of the key (in years) -->

<label for="gnupg_keyexpires"><?cs var:html_escape(Lang.Misc.GnupgKeyExpires) ?>:</label>
	<select name="gnupg_keyexpires" id="gnupg_keyexpires" size="0">
		<option value="0" selected="selected"><?cs
			var:html_escape(Lang.Misc.Never) ?></option>
		<option value="1y">1</option>
		<option value="2y">2</option>
		<option value="3y">3</option>
		<option value="5y">5</option>
		<option value="10y">10</option>
	</select>
<?cs /if ?>

