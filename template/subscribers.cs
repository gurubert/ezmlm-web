<div class="title">
	<h1>
		<?cs if:(Data.List.PartType == "allow") ?>	<?cs var:Lang.Title.AllowList ?>
		<?cs elif:(Data.List.PartType == "deny") ?>	<?cs var:Lang.Title.DenyList ?>
		<?cs elif:(Data.List.PartTyoe == "digest") ?><?cs var:Lang.Title.DigestList ?>
		<?cs elif:(Data.List.PartType == "mod") ?>	<?cs var:Lang.Title.ModList ?>
		<?cs else ?> 								<?cs var:Lang.Title.SubscriberList ?>
		<?cs /if ?>
	</h1>
</div>

<?cs if:((Data.List.PartType == "digest") || (Data.List.PartType == "deny")) ?>
  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">

	<input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>" />
	
	<ul>
	<?cs if:(Data.List.PartType == "digest") ?>
		<li><?cs call:checkbox("d") ?></li>
		<li><?cs call:setting("4") ?></li>
	<?cs elif:(Data.List.PartType == "deny") ?>
		<li><?cs call:checkbox("k") ?></li>
	<?cs /if ?>

	<!-- include default form values -->
	<?cs include:TemplateDir + '/form_common.cs' ?>

	<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
	</ul>
	<br/>
<?cs /if ?>
	

<?cs if:(Data.List.hasPostMod || Data.List.hasSubMod || Data.List.hasRemoteAdmin) ?>
	<!-- show warnings for wrong moderation paths -->
	<!-- TODO: check mod_path -->
	<?cs include:TemplateDir + "modpath_info.cs" ?>
<?cs /if ?>


<div class="subscribers">

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />
	    <?cs if:Data.List.PartType ?>
		    <input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>" />
	    <?cs /if ?>

		<ul>
		
			<?cs if:subcount(Data.List.Subscribers) > 0 ?>
			<!-- scrollbox for list's subscribers -->
			<!-- Keep selection box a reasonable size - suggested by Sebastian Andersson -->
				<?cs if:subcount(Data.List.Subscribers) > 25 ?>
					<?cs set:Data.ScrollSize = 25 ?>
				  <?cs else ?>
					<?cs set:Data.ScrollSize = subcount(Data.List.Subscribers) ?>
				<?cs /if ?>
				<li><select name="mailaddress_del" tabindex="1"
						size="<?cs var:Data.ScrollSize ?>" multiple="multiple">
					<?cs each:item = Data.List.Subscribers ?>
						<option><?cs var:item ?></option>
					<?cs /each ?>
				</select></li>
			<?cs else ?>
				<li><?cs var:Lang.Misc.NoSubscribers ?></li>
			<?cs /if ?>
	
		<?cs if:subcount(Data.List.Subscribers) > 0 ?> 
		    <li><?cs var:subcount(Data.List.Subscribers) ?> <?cs var:Lang.Misc.Subscribers ?></li>
			<li><button class="add_remove" type="submit" name="action" tabindex="2" value="address_del"><?cs var:Lang.Buttons.DeleteAddress ?></button></li>
		<?cs /if ?>

		<li class="formfield"><?cs var:Lang.Misc.AddSubscriberAddress ?>
			<ul><li><input type="text" name="mailaddress_add"
				<?cs call:help_title("AddAddress") ?> tabindex="3" size="40" /></li>
			</ul></li>
		<?cs if:Data.Permissions.FileUpload ?>
		    <li class="formfield"><?cs var:Lang.Misc.AddSubscriberFile ?>
			<ul><li><input type="file" name="mailaddressfile" size="20"
				<?cs call:help_title("AddAddressFile") ?> maxlength="100" tabindex="4" /></li>
			</ul></li>
		<?cs /if ?>

		<button type="submit" tabindex="5" name="action" value="address_add"><?cs var:Lang.Buttons.AddAddress ?></button>
		</ul>
	    </div>

	</form>

    </div>

</div>
