from tree.models import PartnersMapper, PartnersGet


def get_partner(partner: PartnersMapper, other_id: str):
    return PartnersGet(partner_id=partner.husband_id if partner.wife_id == other_id else partner.wife_id,
                       wedding_date=partner.wedding_date, divorce_date=partner.divorce_date)
