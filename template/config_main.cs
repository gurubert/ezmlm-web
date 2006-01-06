<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigMain) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigMain) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ConfigMain) ?> </legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="config_subset" value="main" />

		<ul>

			<!-- list language -->
			<?cs if:subcount(Data.List.AvailableLanguages) > 0 ?>
				<li><label for="list_language"><?cs var:html_escape(Lang.Misc.ListLanguage)
						?>:</label>
					<select name="list_language" id="list_language">
						<?cs each:item = Data.List.AvailableLanguages ?>
							<option <?cs if:(item == Data.List.Language)
								?>selected="selected"<?cs /if ?>><?cs var:item ?></option>
						<?cs /each ?>
					</select></li><?cs /if ?>

			<!-- charset -->
			<?cs if:Data.useCharSet ?>
				<li><label for="list_charset"><?cs var:html_escape(Lang.Misc.ListCharset)
						?>:</label>
					<input type="text" name="list_charset" id="list_charset" size="30"
						value="<?cs var:Data.List.CharSet ?>" />
					</li><?cs /if ?>

			<!-- list owner address -->
			<li><?cs call:setting("5") ?></li>

			<!-- set main list name -->
			<li><?cs call:setting("0") ?></li>

			<!-- process mailman-style requests -->
			<li><?cs call:checkbox("q") ?></li>

			<!-- remove ezmlm-warn -->
			<li><?cs call:checkbox("w") ?></li>

			<!-- mysql database -->
			<?cs if:Data.Modules.mySQL ?>
				<li><?cs call:setting("6") ?></li><?cs /if ?>

			<!-- ezmlm-web administators -->
			<?cs if:Data.WebUser.show && Data.List.WebUsers ?>
				<li><?cs var:html_escape(Lang.Misc.AllowedToEdit) ?>
					<ul><li><input type="text"
					name="webusers" value="<?cs var:html_escape(Data.List.WebUsers)
					?>" size="40" /><br/>
					</li></ul></li><?cs /if ?>

			<li><!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

			<input type="hidden" name="action" value="config_do" />
			<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button></li>
		</ul>

	</form>

</fieldset>
