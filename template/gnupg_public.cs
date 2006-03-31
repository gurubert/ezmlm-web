<div class="title">
	<h1><?cs var:html_escape(Lang.Title.GnupgPublic) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.GnupgPublic) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.GnupgPublic) ?> </legend>

	<form method="post" action="<?cs call:link("","","","","","") ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="gnupg_subset" value="public" />

		<?cs call:show_options(UI.Options.Keymanagement.Public) ?>

		<?cs if:subcount(Data.List.gnupg_keys.public) > 0 ?>
			<ul>
			<?cs each:key = Data.List.gnupg_keys.public
				?><li><?cs var:name(key) ?> - <?cs var:key ?></li>
				<?cs /each ?>
			</ul><?cs /if ?>

		<!-- include default form values -->
		<?cs include:TemplateDir + '/form_common.cs' ?>

		<input type="hidden" name="action" value="gnupg_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateGnupg) ?></button>

	</form>

</fieldset>
