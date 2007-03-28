<div class="title">
	<h1>
		<?cs if:(Data.List.PartType == "allow") ?>	<?cs var:html_escape(Lang.Title.AllowList) ?>
		<?cs elif:(Data.List.PartType == "deny") ?>	<?cs var:html_escape(Lang.Title.DenyList) ?>
		<?cs elif:(Data.List.PartType == "digest") ?><?cs var:html_escape(Lang.Title.DigestList) ?>
		<?cs elif:(Data.List.PartType == "mod") ?>	<?cs var:html_escape(Lang.Title.ModList) ?>
		<?cs else ?> 								<?cs var:html_escape(Lang.Title.SubscriberList) ?>
		<?cs /if ?>
	</h1>
</div>

<div class="introduction">
	<p>
		<?cs if:(Data.List.PartType == "allow") ?>	<?cs var:html_escape(Lang.Introduction.AllowList) ?>
		<?cs elif:(Data.List.PartType == "deny") ?>	<?cs var:html_escape(Lang.Introduction.DenyList) ?>
		<?cs elif:(Data.List.PartType == "digest") ?><?cs var:html_escape(Lang.Introduction.DigestList) ?>
		<?cs elif:(Data.List.PartType == "mod") ?>	<?cs var:html_escape(Lang.Introduction.ModList) ?>
		<?cs else ?> 							<?cs var:html_escape(Lang.Introduction.SubscriberList) ?>
		<?cs /if ?>
	</p>
</div>

<?cs if:Data.List.PartType == 'mod' ?>
	<!-- show warnings for wrong moderation paths -->
	<?cs include:TemplateDir + "modpath_info.cs" ?>
<?cs /if ?>


<?cs if:(	((Data.List.PartType == "digest")
				&& (subcount(UI.Options.Subscribers.Digest) >0)) 
			|| ((Data.List.PartType == "deny")
				&& (subcount(UI.Options.Subscribers.Deny) >0))
			|| ((Data.List.PartType == 'mod')
				&& (subcount(UI.Options.Subscribers.Moderators) >0))) ?>

	<fieldset class="form">
		<legend><?cs var:html_escape(Lang.Legend.RelevantOptions) ?> </legend>

	<form method="post" action="<?cs call:link("","","","","","") ?>" enctype="application/x-www-form-urlencoded">

		<input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>" />
		
			<?cs if:(Data.List.PartType == "digest") ?>
				<?cs call:show_options(UI.Options.Subscribers.Digest) ?>
			<?cs elif:(Data.List.PartType == "deny") ?>
				<?cs call:show_options(UI.Options.Subscribers.Deny) ?>
			<?cs elif:(Data.List.PartType == "mod") ?>
				<?cs call:show_options(UI.Options.Subscribers.Moderators) ?>
			<?cs /if ?>

			<!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

			<input type="hidden" name="config_subset" value="RESERVED-subscribers" />
			<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />
			<input type="hidden" name="action" value="config_do" />
			<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button>
	</form>
	</fieldset>
<?cs /if ?>
	

<!-- check, if we should display a subscribers list -->
<?cs if:!Data.List.PartType || (Data.List.PartType == '') ||
	(Data.List.PartType == 'allow') ||
	(Data.List.PartType == 'mod') ||
	((Data.List.PartType == 'deny') && (Data.List.Options.k == 1)) ||
	((Data.List.PartType == 'digest') && (Data.List.Options.d == 1)) ?>

	<fieldset class="form">
		<legend>
			<?cs if:(Data.List.PartType == "allow") ?>	<?cs var:html_escape(Lang.Legend.MembersAllow) ?>
			<?cs elif:(Data.List.PartType == "deny") ?>	<?cs var:html_escape(Lang.Legend.MembersDeny) ?>
			<?cs elif:(Data.List.PartType == "digest") ?><?cs var:html_escape(Lang.Legend.MembersDigest) ?>
			<?cs elif:(Data.List.PartType == "mod") ?>	<?cs var:html_escape(Lang.Legend.MembersMod) ?>
			<?cs else ?> 								<?cs var:html_escape(Lang.Legend.MembersList) ?>
			<?cs /if ?>
		</legend>

	<table class="subscribers"><tr>
	<?cs if:subcount(Data.List.Subscribers) > 0 ?>
		<td><form method="post" action="<?cs call:link("","","","","","") ?>" enctype="application/x-www-form-urlencoded">
			<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />
			<?cs if:Data.List.PartType ?>
				<input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>" />
			<?cs /if ?>

			<ul>
				<!-- scrollbox for list's subscribers -->
				<!-- Keep selection box a reasonable size - suggested by Sebastian Andersson -->
				<?cs if:subcount(Data.List.Subscribers) > 15 ?>
					<?cs set:Data.ScrollSize = 15 ?>
				  <?cs else ?>
					<?cs set:Data.ScrollSize = subcount(Data.List.Subscribers) ?>
				<?cs /if ?>
				<li><select name="mailaddress_del"
						size="<?cs var:Data.ScrollSize ?>" multiple="multiple">
					<?cs each:item = Data.List.Subscribers ?>
						<option value="<?cs var:item.address ?>"><?cs var:item.address ?><?cs if:item.name ?> (<?cs var:item.name ?>)<?cs /if ?></option>
					<?cs /each ?>
				</select></li>
				<li><?cs var:subcount(Data.List.Subscribers) ?> <?cs var:html_escape(Lang.Misc.Subscribers) ?></li>
				<li><input type="hidden" name="action" value="address_del" />
				<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.DeleteAddress) ?></button></form></li>
				<li><form method="post" action="<?cs call:link('','','','','','')
						?>" enctype="application/x-www-form-urlencoded">
					<input type="hidden" name="list" value="<?cs
							var:Data.List.Name ?>" />
					<input type="hidden" name="action" value="download_subscribers" />
					<?cs if:Data.List.PartType ?>
						<input type="hidden" name="part" value="<?cs
								var:Data.List.PartType ?>" /><?cs /if ?>
					<button type="submit" name="send" value="do"><?cs
							var:html_escape(Lang.Buttons.DownloadSubscribersList)
							?></button></form></li>
		</ul></td>
	<?cs /if ?>

	<td><form method="post" action="<?cs call:link("","","","","","") ?>" enctype="multipart/form-data">
		<!-- this form has to be "multipart/form-data" to make file upload work -->
		<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />
		<?cs if:Data.List.PartType ?>
			<input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>" />
		<?cs /if ?>

		<fieldset>
			<ul>
				<li><?cs var:html_escape(Lang.Misc.AddSubscriberAddress) ?>
					<ul><li><input type="text" name="mailaddress_add" size="40" /></li>
					</ul></li>
				<?cs if:Data.Permissions.FileUpload ?>
					<li><?cs var:html_escape(Lang.Misc.AddSubscriberFile) ?>
					<ul><li><input type="file" name="mailaddressfile" size="20"
						maxlength="200" /></li>
					</ul></li>
				<?cs /if ?>
			</ul>
		</fieldset>

		<input type="hidden" name="action" value="address_add" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.AddAddress) ?></button>
	</form></td></tr>
	</table>

	</fieldset>

<?cs /if ?>

