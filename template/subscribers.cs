<div class="subscribers">

    <div class="title">

		<h1><?cs var:Data.List.Name ?></h1>
        <h2>
			<?cs if:(Data.List.PartType == "allow") ?>	<?cs var:Lang.Title.AllowList ?>
			<?cs elif:(Data.List.PartType == "deny") ?>	<?cs var:Lang.Title.DenyList ?>
			<?cs elif:(Data.List.PartTyoe == "digest") ?><?cs var:Lang.Title.DigestList ?>
			<?cs elif:(Data.List.PartType == "mod") ?>	<?cs var:Lang.Title.ModList ?>
			<?cs else ?> 								<?cs var:Lang.Title.SubscriberList ?>
			<?cs /if ?>
		</h2>
        <h3><?cs var:Data.List.Address ?></h3>
	<hr/>
    </div>

	<?cs if:((Data.List.PartType == "digest") || (Data.List.PartType == "deny")) ?>
	  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">

		<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
		<input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>" />
		<?cs if:(Data.List.PartType == "digest") ?>
			<input type="checkbox" name="option_d" value="option_d" <?cs if:Data.List.Options.d ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.d ?></input>
		<?cs elif:(Data.List.PartType == "deny") ?>
			<input type="checkbox" name="option_k" value="option_k" <?cs if:Data.List.Options.k ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.k ?></input>
		<?cs /if ?>

		<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
	<?cs /if ?>
		

    <?cs if:(Data.List.hasPostMod || Data.List.hasSubMod || Data.List.hasRemoteAdmin) ?>
		<!-- show warnings for wrong moderation paths -->
		<?cs include:TemplateDir + "modpath_info.cs" ?>
    <?cs /if ?>


    <div class="list">
	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />
	    <?cs if:Data.List.PartType ?>
		    <input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>" />
	    <?cs /if ?>

	    <!-- scrollbox for list's subscribers -->
	    <!-- Keep selection box a reasonable size - suggested by Sebastian Andersson -->
	    <?cs if:subcount(Data.List.Subscribers) > 25 ?>
		<?cs set:Data.ScrollSize = 25 ?>
	      <?cs else ?>
		<?cs set:Data.ScrollSize = subcount(Data.List.Subscribers) ?>
	    <?cs /if ?>
	    <!-- TODO: this div should float to left - the buttons should be at the right -->
	    <select name="mailaddress_del" tabindex="1" size="<?cs var:Data.ScrollSize ?>" multiple="multiple">
		<?cs each:item = Data.List.Subscribers ?>
		    <option><?cs var:item ?></option>
		<?cs /each ?>
	    </select>
	
	    <div class="add_remove">
		<?cs if:subcount(Data.List.Subscribers) > 0 ?> 
		    <p><?cs var:subcount(Data.List.Subscribers) ?> <?cs var:Lang.Misc.Subscribers ?></p>
		    <button type="submit" name="action" tabindex="2" value="address_del"><?cs var:Lang.Buttons.DeleteAddress ?></button>
		<?cs /if ?>
		<!-- TODO: das helper icon ist erst in der naechsten Zeile -->
		<p class="formfield"><input type="text" name="mailaddress_add"
			<?cs call:help_title("AddAddress") ?>
			tabindex="3" size="40" /><?cs call:help_icon("AddAddress") ?></p>
		<!-- TODO: eventuell ein BR einfuegen -->
		<?cs if:Data.Permissions.FileUpload ?>
		    <p class="formfield"><input type="file" name="mailaddressfile" size="20"
			<?cs call:help_title("AddAddressFile") ?>
			maxlength="100" tabindex="4" /><?cs call:help_icon("AddAddressFile") ?></p>
		<?cs /if ?>
		<button type="submit" tabindex="5" name="action" value="address_add"><?cs var:Lang.Buttons.AddAddress ?></button>
	    </div>

	</form>

    </div>

</div>
