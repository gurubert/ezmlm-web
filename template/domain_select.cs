<div class="title">
	<h1><?cs var:html_escape(Lang.Title.DomainSelect) ?></h1>
</div>

<fieldset>
	<legend>
		<?cs var:html_escape(Lang.Legend.AvailableDomains) ?>
	</legend>

<?cs if:subcount(Data.Domains) > 0 ?>
	<ul>
	<?cs each:domain = Data.Domains
		?><li><a href="<?cs call:link('domain',name(domain),'','','','')
			?>"><?cs var:html_escape(domain) ?></a></li>
	<?cs /each ?>
	</ul>
<?cs else ?>
	<p><?cs var:html_escape(Lang.Misc.NoDomainsAvailable) ?></p>
<?cs /if ?>

</fieldset>

