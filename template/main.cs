<!-- $Id$ -->

<?cs include:TemplateDir + '/macros.cs' ?>
<?cs include:TemplateDir + '/header.cs' ?>

<!-- this ezmlm-web template follows: <?cs var:Data.Action ?> -->

<?cs if:Data.Error ?>
	<?cs call:error(Data.Error) ?>
<?cs else ?>
	<?cs include:TemplateDir + '/nav.cs' ?>
	<?cs if:Data.Warning ?><?cs call:warning(Data.Warning) ?><?cs /if ?>
	<?cs if:Data.Success ?><?cs call:success(Data.Success) ?><?cs /if ?>
	<?cs include:TemplateDir + '/' + Data.Action + '.cs' ?>
<?cs /if ?>

<?cs include:TemplateDir + '/footer.cs' ?>
