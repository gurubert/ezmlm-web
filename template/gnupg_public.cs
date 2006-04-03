<div class="title">
	<h1><?cs var:html_escape(Lang.Title.GnupgPublic) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.GnupgPublic) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.GnupgKeyImport) ?> </legend>
	<form method="post" action="<?cs call:link("","","","","","") ?>"
		enctype="application/x-www-form-urlencoded">

		<input type="hidden" name="gnupg_subset" value="public" />

		<?cs call:show_options(UI.Options.Keymanagement.Public) ?>

		<td><form method="post" action="<?cs call:link("","","","","","") ?>"
			enctype="multipart/form-data">
		<!-- this form has to be "multipart/form-data" to make file upload work -->
		<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />

		<ul>
			<li><?cs var:html_escape(Lang.Misc.GnupgImportKey) ?>
				<ul><li><input type="file" name="gnupg_key_file" size="50"
					maxlength="250" /></li>
				</ul>
			</li>

			<li>
				<!-- include default form values -->
				<?cs include:TemplateDir + '/form_common.cs' ?>

				<input type="hidden" name="action" value="gnupg_import_key" />
				<button type="submit" name="send" value="do"><?cs
					var:html_escape(Lang.Buttons.GnupgImportKey) ?></button>
			</li>
		</ul>
	
	</form>

</fieldset>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.GnupgPublicKeys) ?> </legend>

	<?cs if:subcount(Data.List.gnupg_keys.public) > 0 ?>

		<form method="post" action="<?cs call:link("","","","","","") ?>"
			enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="gnupg_subset" value="public" />

		<table>
			<?cs each:key = Data.List.gnupg_keys.public
				?><tr><td><input type="checkbox" name="gnupg_key_<?cs var:key.id ?>"
					id="gnupg_key_<?cs var:key.id ?>" /></td>
					<td><label for="gnupg_key_<?cs var:key.id ?>"><?cs
						var:html_escape(key.name) ?></label></td>
					<td><label for="gnupg_key_<?cs var:key.id ?>"><?cs
						var:html_escape(key.email) ?></label></td>
					<td><label for="gnupg_key_<?cs var:key.id ?>"><?cs
						var:html_escape(key.expires) ?></label></td>
					</tr>
			<?cs /each ?>
		</table>

		<!-- include default form values -->
		<?cs include:TemplateDir + '/form_common.cs' ?>

		<input type="hidden" name="action" value="gnupg_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.DeletePublicKey) ?></button>

	</form>
	<?cs else ?>
		<p><? var:html_escape(Lang.Misc.NoPublicKeys ?></p>
	<?cs /if ?>

</fieldset>
