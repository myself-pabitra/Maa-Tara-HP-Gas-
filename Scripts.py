from SubDealers.models import Subdealer
for s in Subdealer.objects.filter(subdealerCode__isnull=True):
    s.subdealerCode = s.create_subdealer_code()
    s.save()
