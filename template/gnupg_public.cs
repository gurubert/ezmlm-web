<div class="title">
	<h1><?cs var:html_escape(Lang.Title.GnupgPublic) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.GnupgPublic) ?></p>
</div>

<?cs include:TemplateDir + '/gnupg_import.cs' ?>

<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.GnupgPublicKeys) ?> </legend>

	<?cs if:subcount(Data.List.gnupg_keys.public) > 0 ?>

	<?cs call:form_header("gnupg_public_keys", "") ?>
		<input type="hidden" name="gnupg_subset" value="public" />

		<table class="gnupg_keys">
			<?cs each:key = Data.List.gnupg_keys.public
				?><tr><td><input type="checkbox" name="gnupg_key_<?cs var:key.id ?>"
					id="gnupg_key_<?cs var:key.id ?>" /></td>
					<td><label for="gnupg_key_<?cs var:key.id ?>"><?cs
						var:html_escape(key.name) ?></label></td>
					<td><label for="gnupg_key_<?cs var:key.id ?>"><?cs
						var:html_escape(key.email) ?></label></td>
					<td><label for="gnupg_key_<?cs var:key.id ?>"><?cs
						if:key.expires ?><?cs var:html_escape(key.expires) ?><?cs
						else ?><?cs var:html_escape(Lang.Misc.Never) ?><?cs /if
						?></label></td>
					<td><a href="<?cs call:link("action", "gnupg_export",
									"list", Data.List.Name,
									"gnupg_keyid", key.id) ?>"
							title="<?cs var:html_escape(Lang.Buttons.GnupgExportKey)
								?>"><?cs var:html_escape(Lang.Buttons.GnupgExportKey)
								?></a></td>
					</tr>
			<?cs /each ?>
		</table>

		<input type="hidden" name="action" value="gnupg_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.DeletePublicKey) ?></button>

	</form>
	<?cs else ?>
		<p><?cs var:html_escape(Lang.Misc.GnupgNoPublicKeys) ?></p>
	<?cs /if ?>

</fieldset>
