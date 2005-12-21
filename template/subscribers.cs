<div class="title">
	<h1>
		<?cs if:(Data.List.PartType == "allow") ?>	<?cs var:Lang.Title.AllowList ?>
		<?cs elif:(Data.List.PartType == "deny") ?>	<?cs var:Lang.Title.DenyList ?>
		<?cs elif:(Data.List.PartType == "digest") ?><?cs var:Lang.Title.DigestList ?>
		<?cs elif:(Data.List.PartType == "mod") ?>	<?cs var:Lang.Title.ModList ?>
		<?cs else ?> 								<?cs var:Lang.Title.SubscriberList ?>
		<?cs /if ?>
	</h1>
</div>

<div class="introduction">
	<p>
		<?cs if:(Data.List.PartType == "allow") ?>	<?cs var:Lang.Introduction.AllowList ?>
		<?cs elif:(Data.List.PartType == "deny") ?>	<?cs var:Lang.Introduction.DenyList ?>
		<?cs elif:(Data.List.PartType == "digest") ?><?cs var:Lang.Introduction.DigestList ?>
		<?cs elif:(Data.List.PartType == "mod") ?>	<?cs var:Lang.Introduction.ModList ?>
		<?cs else ?> 							<?cs var:Lang.Introduction.SubscriberList ?>
		<?cs /if ?>
	</p>
</div>

<?cs if:Data.List.PartType == 'mod' ?>
	<!-- show warnings for wrong moderation paths -->
	<?cs include:TemplateDir + "modpath_info.cs" ?>
<?cs /if ?>


<?cs if:((Data.List.PartType == "digest") || (Data.List.PartType == "deny") || (Data.List.PartType == 'mod')) ?>

	<fieldset class="form">
		<legend><?cs var:Lang.Legend.RelevantOptions ?></legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">

		<input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>" />
		
		<ul>
			<?cs if:(Data.List.PartType == "digest") ?>
				<li><?cs call:checkbox("d") ?></li>
				<li><?cs call:setting("4") ?></li>
			<?cs elif:(Data.List.PartType == "deny") ?>
				<li><?cs call:checkbox("k") ?></li>
			<?cs elif:(Data.List.PartType == "mod") ?>
				<li><?cs call:setting("7") ?></li>
				<li><?cs call:setting("8") ?></li>
			<?cs /if ?>

			<!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

			<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
		</ul>
	</form>
	</fieldset>
<?cs /if ?>
	

<div class="subscribers">

	<fieldset class="form">
		<legend><?cs var:Lang.Legend.Subscription ?></legend>

	<!-- this form has to be "multipart/form-data" to make file upload work -->
	<form method="post" action="<?cs var:ScriptName ?>" enctype="multipart/form-data">
	    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />
	    <?cs if:Data.List.PartType ?>
		    <input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>" />
	    <?cs /if ?>

		<table class="subscribers"><tr>
		<?cs if:subcount(Data.List.Subscribers) > 0 ?>
			<td><ul>
			<!-- scrollbox for list's subscribers -->
			<!-- Keep selection box a reasonable size - suggested by Sebastian Andersson -->
				<?cs if:subcount(Data.List.Subscribers) > 15 ?>
					<?cs set:Data.ScrollSize = 15 ?>
				  <?cs else ?>
					<?cs set:Data.ScrollSize = subcount(Data.List.Subscribers) ?>
				<?cs /if ?>
				<li><select name="mailaddress_del" tabindex="1"
						size="<?cs var:Data.ScrollSize ?>" multiple="multiple">
					<?cs each:item = Data.List.Subscribers ?>
						<option><?cs var:item ?></option>
					<?cs /each ?>
				</select></li>
				<li><?cs var:subcount(Data.List.Subscribers) ?> <?cs var:Lang.Misc.Subscribers ?></li>
				<li><button class="add_remove" type="submit" name="action" tabindex="2" value="address_del"><?cs var:Lang.Buttons.DeleteAddress ?></button></li>
			</ul></td>
		<?cs /if ?>

		<td><ul>

			<li><?cs var:Lang.Misc.AddSubscriberAddress ?>
				<ul><li><input type="text" name="mailaddress_add"
					<?cs call:help_title("AddAddress") ?> tabindex="3" size="40" /></li>
				</ul></li>
			<?cs if:Data.Permissions.FileUpload ?>
				<li><?cs var:Lang.Misc.AddSubscriberFile ?>
				<ul><li><input type="file" name="mailaddressfile" size="20"
					<?cs call:help_title("AddAddressFile") ?> maxlength="100" tabindex="4" /></li>
				</ul></li>
			<?cs /if ?>

			<button type="submit" tabindex="5" name="action" value="address_add"><?cs var:Lang.Buttons.AddAddress ?></button>
		</ul></td></tr></table>

	</form>
	</fieldset>
</div>

