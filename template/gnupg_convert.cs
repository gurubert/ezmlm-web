<div class="title">
	<h1><?cs var:html_escape(Lang.Title.GnupgConvert) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.GnupgConvert) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.GnupgConvert) ?> </legend>

	<form method="post" action="<?cs call:link("","","","","","") ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />

		<input type="hidden" name="action" value="gnupg_convert_do" />
		<button type="submit" name="send" value="do"><?cs
			if:Data.List.Type == "gnupg" ?><?cs
				var:html_escape(Lang.Buttons.GnupgConvertToNormal) ?><?cs
			else ?><?cs
				var:html_escape(Lang.Buttons.GnupgConvertToEncrypted) ?><?cs
			/if ?></button>
	</form>

</fieldset>
