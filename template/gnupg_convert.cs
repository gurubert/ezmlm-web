<div class="title">
	<h1><?cs var:html_escape(Lang.Title.GnupgConvert) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.GnupgConvert) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.GnupgConvert) ?> </legend>

	<?cs call:form_header("gnupg_convert", "") ?>
		<?cs if:Data.List.Features.Crypto
			?><button type="submit" name="send" value="do"><?cs
			var:html_escape(Lang.Buttons.GnupgConvertToPlain) ?></button>
			<input type="hidden" name="action" value="gnupg_convert_disable" /><?cs
		else
			?><button type="submit" name="send" value="do"><?cs
			var:html_escape(Lang.Buttons.GnupgConvertToEncrypted) ?></button>
			<input type="hidden" name="action" value="gnupg_convert_enable" /><?cs
		/if ?>
	</form>

</fieldset>
