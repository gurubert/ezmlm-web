<div class="title">
	<h1><?cs var:html_escape(Lang.Title.GpgEzmlmConvert) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.GpgEzmlmConvert) ?></p>
</div>

<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.GpgEzmlmConvert) ?> </legend>

	<?cs call:form_header("gpgezmlm_convert") ?>
	<ul><li>
		<?cs if:Data.List.Features.GpgEzmlm
			?><button type="submit" name="send" value="do"><?cs
			var:html_escape(Lang.Buttons.GpgEzmlmConvertToPlain) ?></button>
			<input type="hidden" name="action" value="gpgezmlm_convert_disable" /><?cs
		else
			?><button type="submit" name="send" value="do"><?cs
			var:html_escape(Lang.Buttons.GpgEzmlmConvertToEncrypted) ?></button>
			<input type="hidden" name="action" value="gpgezmlm_convert_enable" /><?cs
		/if ?>
	</li></ul>
	</form>

</fieldset>
