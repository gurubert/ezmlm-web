<!-- $Id$ -->

<div id="nav_bar">

<ul>
	<?cs if:(subcount(Data.Domains) > 0) && (UI.Navigation.DomainSelect == 1) ?>
		<li><a <?cs if:(Data.Action == "domain_select") ?> class="nav_active"<?cs /if ?>
			href="<?cs call:link('action','domain_select','','','','') ?>"
			title="<?cs var:html_escape(Lang.Menue.DomainSelect) ?>"><?cs
			var:html_escape(Lang.Menue.DomainSelect) ?></a>
		</li>
		<?cs /if ?>
	<?cs if:(subcount(Data.Lists) > 0) && (UI.Navigation.ListSelect == 1) ?>
		<li><a <?cs if:(Data.Action == "list_select") ?> class="nav_active"<?cs /if ?>
			href="<?cs call:link("action","list_select","","","","") ?>"
			title="<?cs var:html_escape(Lang.Menue.ListSelect) ?>"><?cs var:html_escape(Lang.Menue.ListSelect) ?></a>
		</li>
		<?cs /if ?>
	<?cs if:Data.Permissions.Create && (UI.Navigation.ListCreate == 1) ?>
		<li><a <?cs if:(Data.Action == "list_create") ?> class="nav_active"<?cs /if ?>
			href="<?cs call:link("action","list_create_ask","","","","") ?>"
			title="<?cs var:html_escape(Lang.Menue.ListCreate) ?>"><?cs var:html_escape(Lang.Menue.ListCreate) ?></a>
		</li>
		<?cs /if ?>

	<?cs if:((subcount(Data.Lists) > 0) && (UI.Navigation.ListSelect == 1))
			|| (Data.Permissions.Create && (UI.Navigation.ListCreate == 1)) ?>
		<li><hr/></li>
	<?cs /if ?>


<?cs if:Data.List.Name ?>

	<li><font class="no_link"><?cs var:html_escape(Lang.Menue.Properties) ?> <?cs call:limit_string_len(html_escape(Data.List.Name),25) ?></font><ul><li>
		<?cs if:UI.Navigation.Subscribers.Subscribers == 1
				?><a <?cs if:((Data.Action == "subscribers")
						&& ((Data.List.PartType == "") || !Data.List.PartType))
					?>class="nav_active"<?cs /if ?>
			href="<?cs call:link("list",Data.List.Name,"action","subscribers","","") ?>"
				title="<?cs var:html_escape(Lang.Menue.Subscribers) ?>"><?cs
			else ?><font class="no_link"><?cs /if ?><?cs
				var:html_escape(Lang.Menue.Subscribers) ?><?cs
			if:UI.Navigation.Subscribers.Subscribers == 1 ?></a><?cs else ?></font><?cs
				/if ?>
			<ul>
				<?cs if:UI.Navigation.Subscribers.Allow == 1
					?><li><a <?cs if:((Data.Action == "subscribers") &&
						(Data.List.PartType == "allow")) ?>class="nav_active"<?cs /if ?>
					href="<?cs call:link("list",Data.List.Name,"action","subscribers",
							"part","allow") ?>"><?cs
						var:html_escape(Lang.Menue.AllowList) ?></a></li><?cs /if ?>
				<?cs if:UI.Navigation.Subscribers.Deny == 1
					?><li><a <?cs if:((Data.Action == "subscribers") &&
						(Data.List.PartType == "deny")) ?> class="nav_active"<?cs /if ?>
					href="<?cs call:link("list",Data.List.Name,"action","subscribers",
							"part","deny") ?>"><?cs
						var:html_escape(Lang.Menue.DenyList) ?></a></li><?cs /if ?>
				<?cs if:UI.Navigation.Subscribers.Digest == 1
					?><li><a <?cs if:((Data.Action == "subscribers") &&
						(Data.List.PartType == "digest")) ?> class="nav_active"<?cs /if ?>
					href="<?cs call:link("list",Data.List.Name,"action","subscribers",
							"part","digest") ?>"><?cs
						var:html_escape(Lang.Menue.DigestList) ?></a></li><?cs /if ?>
				<?cs if:UI.Navigation.Subscribers.Moderators == 1
					?><li><a <?cs if:((Data.Action == "subscribers") &&
						(Data.List.PartType == "mod")) ?> class="nav_active"<?cs /if ?>
					href="<?cs call:link("list",Data.List.Name,"action","subscribers",
							"part","mod") ?>"><?cs
						var:html_escape(Lang.Menue.ModList) ?></a></li><?cs /if ?>
			</ul>
		</li>

		<li><?cs if:UI.Navigation.Config.Main == 1
			?><a <?cs if:(Data.Action == "config_main") ?> class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","config_ask",
						"config_subset","main") ?>" title="<?cs
				var:html_escape(Lang.Menue.ConfigMain) ?>"><?cs
			else ?><font class="no_link"><?cs /if ?><?cs
			var:html_escape(Lang.Menue.ConfigMain) ?><?cs
				if UI.Navigation.Config.Main == 1 ?></a><?cs else ?></font><?cs /if ?>
		<ul>
			<?cs if:UI.Navigation.Config.Subscription == 1
				?><li><a <?cs if:(Data.Action == "config_subscription")
					?> class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","config_ask",
						"config_subset","subscription") ?>"
					title="<?cs var:html_escape(Lang.Menue.ConfigSub) ?>"><?cs
					var:html_escape(Lang.Menue.ConfigSub) ?></a></li><?cs /if ?>
			<?cs if:UI.Navigation.Config.Posting == 1
				?><li><a <?cs if:(Data.Action == "config_posting")
					?> class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","config_ask",
					"config_subset","posting") ?>" title="<?cs
					var:html_escape(Lang.Menue.ConfigPost) ?>"><?cs
					var:html_escape(Lang.Menue.ConfigPost) ?></a></li><?cs /if ?>
			<?cs if:UI.Navigation.Config.Processing == 1
				?><li><a <?cs if:(Data.Action == "config_processing")
					?> class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","config_ask",
						"config_subset","processing") ?>"
					title="<?cs var:html_escape(Lang.Menue.ConfigProcess) ?>"><?cs
					var:html_escape(Lang.Menue.ConfigProcess) ?></a></li><?cs /if ?>
			<?cs if:(UI.Navigation.Config.GnupgOptions == 1) &&
					Data.List.Features.Crypto
				?><li><a <?cs if:(Data.Action == "config_encryption")
					?> class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","config_ask",
						"config_subset","encryption") ?>"
					title="<?cs var:html_escape(Lang.Menue.GnupgOptions) ?>"><?cs
					var:html_escape(Lang.Menue.GnupgOptions) ?></a></li><?cs /if ?>
			<?cs if:UI.Navigation.Config.Archive == 1
				?><li><a <?cs if:(Data.Action == "config_archive") ?>
					class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","config_ask",
						"config_subset","archive") ?>"
					title="<?cs var:html_escape(Lang.Menue.ConfigArchive) ?>"><?cs
					var:html_escape(Lang.Menue.ConfigArchive) ?></a></li><?cs /if ?>
			<?cs if:UI.Navigation.Config.Admin == 1
				?><li><a <?cs if:(Data.Action == "config_admin") ?>
					class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","config_ask",
						"config_subset","admin") ?>"
					title="<?cs var:html_escape(Lang.Menue.ConfigAdmin) ?>"><?cs
					var:html_escape(Lang.Menue.ConfigAdmin) ?></a></li><?cs /if ?>
			<?cs if:UI.Navigation.Config.All == 1
				?><li><a <?cs if:(Data.Action == "config_all") ?>
					class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","config_ask",
						"config_subset","all") ?>"
					title="<?cs var:html_escape(Lang.Menue.ConfigAll) ?>"><?cs
					var:html_escape(Lang.Menue.ConfigAll) ?></a></li><?cs /if ?>
		</ul></li>

		<?cs if:(subcount(UI.Navigation.Gnupg) > 0) && (Data.List.Features.Crypto)
				?><li><font class="no_link"><?cs var:html_escape(Lang.Menue.Gnupg)
				?></font>
		<ul>
			<?cs if:UI.Navigation.Gnupg.PublicKeys == 1
				?><li><a <?cs if:(Data.Action == "gnupg_public")
					?> class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","gnupg_ask",
						"gnupg_subset","public") ?>"
					title="<?cs var:html_escape(Lang.Menue.GnupgPublicKeys) ?>"><?cs
					var:html_escape(Lang.Menue.GnupgPublicKeys) ?></a></li><?cs /if ?>
			<?cs if:UI.Navigation.Gnupg.SecretKeys == 1
				?><li><a <?cs if:(Data.Action == "gnupg_secret")
					?> class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","gnupg_ask",
						"gnupg_subset","secret") ?>"
					title="<?cs var:html_escape(Lang.Menue.GnupgSecretKeys) ?>"><?cs
					var:html_escape(Lang.Menue.GnupgSecretKeys) ?></a></li><?cs /if ?>
			<?cs if:UI.Navigation.Gnupg.GenerateKey == 1
				?><li><a <?cs if:(Data.Action == "gnupg_generate_key")
					?> class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","gnupg_ask",
						"gnupg_subset","generate_key") ?>"
					title="<?cs var:html_escape(Lang.Menue.GnupgGenerateKey) ?>"><?cs
					var:html_escape(Lang.Menue.GnupgGenerateKey) ?></a></li><?cs /if ?>
		</ul></li><?cs /if ?>

		<?cs if:UI.Navigation.TextEdit == 1
			?><li><a <?cs if:((Data.Action == "textfiles")
					|| (Data.Action == "textfile_edit")) ?> class="nav_active"<?cs /if ?>
				href="<?cs call:link("list",Data.List.Name,"action","textfiles","","") ?>"
					title="<?cs var:html_escape(Lang.Menue.TextFiles) ?>"><?cs
					var:html_escape(Lang.Menue.TextFiles) ?></a></li><?cs /if ?>

		<?cs if:(UI.Navigation.GnupgConvert == 1) && Config.Features.Crypto
			?><li><a <?cs if:(Data.Action == "gnupg_convert")
				?> class="nav_active"<?cs /if ?>
			href="<?cs call:link("list",Data.List.Name,"action","gnupg_convert_ask","","") ?>"
				title="<?cs var:html_escape(Lang.Menue.GnupgConvert) ?>"><?cs
					var:html_escape(Lang.Menue.GnupgConvert) ?></a></li><?cs /if ?>
		
		<?cs if:UI.Navigation.SubscribeLog == 1
			?><li><a <?cs if:(Data.Action == "show_subscription_log")
				?> class="nav_active"<?cs /if ?>
			href="<?cs call:link("list",Data.List.Name,"action","subscribe_log","","") ?>"
				title="<?cs var:html_escape(Lang.Menue.SubscribeLog) ?>"><?cs
				var:html_escape(Lang.Menue.SubscribeLog) ?></a></li><?cs /if ?>
		<?cs if:UI.Navigation.ListDelete == 1
			?><li><a <?cs if:(Data.Action == "list_delete") ?> class="nav_active"<?cs /if ?>
			href="<?cs call:link("list",Data.List.Name,"action","list_delete_ask","","") ?>"
				title="<?cs var:html_escape(Lang.Menue.ListDelete) ?>"><?cs
				var:html_escape(Lang.Menue.ListDelete) ?></a></li><?cs /if ?>
		
	</ul></li>

	<li><hr/></li>
<?cs /if ?>

	<?cs if:UI.Navigation.Language || UI.Navigation.Interface ?>
		<?cs if:UI.Navigation.Language ?>
			<li><?cs include:TemplateDir + '/language_select.cs' ?></li>
		<?cs /if ?>
		<?cs if:UI.Navigation.Interface ?>
			<li><?cs include:TemplateDir + '/interface_select.cs' ?></li>
		<?cs /if ?>

		<li><hr/></li>

	<?cs /if ?>

	<?cs if:UI.Navigation.Help
		?><li><a href="http://www.ezmlm.org/ezman/index.html#toc1" target="_blank"
		title="<?cs var:html_escape(Lang.Misc.HelpLink) ?>"><?cs
		var:html_escape(Lang.Menue.Help) ?></a></li><?cs /if ?>

</ul>

<!-- end of navbar div -->
</div>

